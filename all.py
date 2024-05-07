import logging
import multiprocessing
from collabLLM import *
from collabAudio import *

logging.basicConfig(level=logging.INFO) # set logging level

def main():	
	# manager = multiprocessing.Manager()
	states = multiprocessing.Array('d', 1) # keep track of states of various processes
	
	while True:
		recording = multiprocessing.Process(target=audio, args=(states,))
		transcribing = multiprocessing.Process(target=transcribe, args=(states,))
		brainstorming = multiprocessing.Process(target=brainstorm, args=(states,))
		
		recording.start() # run audio process
		recording.join() # end audio process
		transcribing.start() # run transcription process
		transcribing.join() # end transcription process
		brainstorming.start() # run concept generation
		brainstorming.join() # end concept generation

if __name__ == '__main__':
	main()

# response = client.images.generate(
#   model="dall-e-3",
#   prompt=responses[2],
#   size="1024x1024",
#   quality="standard",
#   n=1,
# )
# 
# image_url = response.data[0].url
# 
# logging.info(image_url)