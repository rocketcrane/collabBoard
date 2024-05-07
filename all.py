import json
import logging
import multiprocessing
from collabLLM import *
from collabAudio import *
from collabColor import *

theme = "Post-Nuclear Housing Advertising"

logging.basicConfig(level=logging.INFO) # set logging level

def main():	
	# manager = multiprocessing.Manager()
	states = multiprocessing.Array('d', 3) # keep track of states of various processes
	
	# while True:
	recording = multiprocessing.Process(target=audio, args=(states,))
	transcribing = multiprocessing.Process(target=transcribe, args=(states,))
	brainstorming = multiprocessing.Process(target=brainstorm, args=(states,))
	detectingStickies = multiprocessing.Process(target=detectStickies, args=(states,))
	
	recording.start() # run audio process
	recording.join() # end audio process
	transcribing.start() # run transcription process
	transcribing.join() # end transcription process
	detectingStickies.start() # start vision
	detectingStickies.join() # end vision
	brainstorming.start() # run concept generation
	brainstorming.join() # end concept generation
	
	# Read stickies.txt and convert to dictionary
	with open('stickies.txt', 'r') as f:
		stickies = []
		for line in f:
			x, y, w, h, text, dist = line.strip().split(',')
			stickies.append({"x": int(x), "y": int(y), "w": int(w), "h": int(h), "isTheme": False, "text": text})
	
	stickies.append({"x": 0, "y": 0, "w": 0, "h": 0, "isTheme": True, "text": theme}) # theme sticky note
	
	# Read generated_concepts.txt and convert to dictionary
	with open('generated_concepts.txt', 'r') as f:
		concepts = []
		for line in f:
			concepts.append({"details": str(line.strip("\n"))})
			
	# Read image.txt and convert to dictionary
	# with open('image.txt', 'r') as f:
	# 	images = []
	# 	for line in f:
	# 		image_prompt, url = line.strip().split('~')
	# 		images.append({"image_prompt": str(image_prompt), "url": str(url)})
	
	# Read image.txt and convert to dictionary
	with open('image.txt', 'r') as f:
		lines = f.readlines()
		last_two_lines = lines[-2:]
		images = []
		for line in last_two_lines:
			image_prompt, url = line.strip().split('~')
			images.append({"image_prompt": str(image_prompt), "url": str(url)})
	
	# Read summary.txt and convert to dictionary
	with open('summary.txt', 'r') as f:
		summary = []
		for line in f:
			summary.append({"title": "Summary", "details": str(line.strip("\n"))})
	
	# Combine dictionaries
	data = {"stickies": stickies, "generated_concepts": concepts, "generated_images": images, "generated_summary": summary}
	
	# Write to JSON file
	with open('UI/public/data_new.json', 'w') as f:
		json.dump(data, f, indent=4)

if __name__ == '__main__':
	main()