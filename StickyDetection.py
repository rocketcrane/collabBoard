import cv2
import numpy as np

# Define the range for pink color in HSV
lower_pink = np.array([160, 50, 50])
upper_pink = np.array([180, 255, 255])

def find_pink_squares(image, min_area=1000):
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
                squares.append((center_x, center_y))
    return squares

def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Camera is not available")
        return
    previous_count = 0
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to grab frame")
                break
            current_squares = find_pink_squares(frame)
            current_count = len(current_squares)
            if current_count != previous_count:
                print("Change in number of squares detected.")
                print("Current squares coordinates:", current_squares)
                previous_count = current_count  # Update previous count
            for center in current_squares:
                cv2.circle(frame, center, 5, (0, 255, 0), -1)  # Draw center of squares
            cv2.imshow('Pink Square Detector', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
