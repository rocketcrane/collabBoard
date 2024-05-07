import cv2
import numpy as np
import os
import time
import shutil
import json
import math
import logging
import matplotlib.pyplot as plt
from path import Path
from datetime import datetime
from htr_pipeline import read_page, DetectorConfig, LineClusteringConfig, ReaderConfig, PrefixTree
from PIL import Image

# -------------------------------------------------------------------------------------
def find_pink_squares(image, min_area=1000):
    # Define the range for pink color in HSV
    lower_pink = np.array([160, 50, 50])
    upper_pink = np.array([180, 255, 255])
    
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_pink, upper_pink)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    contours, _ = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    squares = []
    for c in contours:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.04 * peri, True)
        if len(approx) == 4:
            x, y, w, h = cv2.boundingRect(approx)
            area = w * h
            aspect_ratio = w / float(h)
            if area > min_area and 0.8 <= aspect_ratio <= 1.2:
                center_x = x + w // 2
                center_y = y + h // 2
                squares.append((x, y, w, h, center_x, center_y))
    return squares

def save_cropped_image(frame, rect, img_count):
    x, y, w, h = rect
    cropped_img = frame[y:y+h, x:x+w]
    save_path = f'data/cropped_images/cropped_image_{x}_{y}.png'
    cv2.imwrite(save_path, cropped_img)
    return save_path

def resize_image_cv(input_path, output_path, scale_factor):
    img = cv2.imread(input_path)
    new_width = int(img.shape[1] * scale_factor)
    new_height = int(img.shape[0] * scale_factor)
    resized_img = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_CUBIC)
    cv2.imwrite(output_path, resized_img)

def clear_folder(folder_path):
    # Check if the folder exists
    if os.path.exists(folder_path):
        # List all files in the folder
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            try:
                # Check if it is a file and then delete it
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)  # Remove directory and all its contents
            except Exception as e:
                print(f'Failed to delete {file_path}. Reason: {e}')
# -------------------------------------------------------------------------------------

def detectStickies(inputs):
    STICKIES_FILENAME = "stickies.txt" # to save across processes
    try:
        os.remove(STICKIES_FILENAME) # remove the previous stickies
    except:
        logging.warning("no stickies file")

    
    with open('data/words_alpha.txt') as f:
        word_list = [w.strip().upper() for w in f.readlines()]
    prefix_tree = PrefixTree(word_list)
    
    # Define the range for pink color in HSV
    lower_pink = np.array([160, 50, 50])
    upper_pink = np.array([180, 255, 255])
    
    clear_folder('data/cropped_images')
    clear_folder('data/resized_images')
    
    # -------------------------------------------------------------------------------------
    
    for decoder in ['best_path']: # , 'best_path', 'word_beam_search' (dictionary off for best path, on for word beam search)
        cap = cv2.VideoCapture(0)
        # if not cap.isOpened():
        #     print("Error: Camera is not available")
        time.sleep(2)
    
        img_count = 0
        last_count = 0
        last_positions = {}
        stability_duration = 5  # Duration in seconds that the count must be stable before taking a photo
        tolerance = 10  # Tolerance for movement detection
    
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break
    
        squares = find_pink_squares(frame)
        current_count = len(squares)
    
        if current_count != last_count:
            last_count = current_count
            # last_change_time = time.time()
            time.sleep(stability_duration)
    
        for square in squares:
            x, y, w, h, center_x, center_y = square
            center = (center_x, center_y)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            if all(np.linalg.norm(np.array(center) - np.array(last_center)) > tolerance for last_center in last_positions.keys()):
                saved_path = save_cropped_image(frame, (x, y, w, h), img_count)
                resized_path = f'data/resized_images/{x}_{y}_{w}_{h}.jpg'
                resize_image_cv(saved_path, resized_path, 10)
                img_count += 1
            last_positions[center] = (x, y, w, h)
    
    # -------------------------------------------------------------------------------------
    
        all_text = []  # store all text
    
        for img_filename in Path('data/resized_images').files('*.jpg'):
    
            # read text
            img = cv2.imread(img_filename, cv2.IMREAD_GRAYSCALE)
            read_lines = read_page(img,
                                detector_config=DetectorConfig(scale=0.1, margin=1),
                                line_clustering_config=LineClusteringConfig(min_words_per_line=1),
                                reader_config=ReaderConfig(decoder=decoder, prefix_tree=prefix_tree))
    
            # output text
            page_text = []
    
            for read_line in read_lines:
                line_text = ' '.join(read_word.text for read_word in read_line)
                # print(line_text)
                page_text.append(line_text)
            # Merge the text lists of each image into a string
            # separated by newline characters
            all_text.append('\n'.join(page_text))  
            print(all_text)
            
            c_x = img_filename.removesuffix(".jpg").removeprefix("data/resized_images/").split("_")[0]
            c_y = img_filename.removesuffix(".jpg").removeprefix("data/resized_images/").split("_")[1]
            c_w = img_filename.removesuffix(".jpg").removeprefix("data/resized_images/").split("_")[2]
            c_h = img_filename.removesuffix(".jpg").removeprefix("data/resized_images/").split("_")[3]
            
            dist = math.sqrt((int(c_x) - 898)**2 + (int(c_y) - 426)**2)
            
            # save the center coordinates to a text file
            with open(STICKIES_FILENAME, 'a') as f:
                f.write(str(c_x) + ", " + str(c_y) + ", " + str(c_w) + ", " + str(c_h) + ", " + ' '.join(page_text) + ", " + str(dist))
                f.write('\n')
    
            time.sleep(3)
    
            img_count += 1
    inputs[2] = 1 # tell the brainstorming loop that the stickies have been updated