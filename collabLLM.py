import os
import logging
from openai import OpenAI
from datetime import datetime
from dotenv import load_dotenv

load_dotenv() # use .env file for API key
client = OpenAI() # initialize AI

def transcribe(inputs):
	MP3_FILENAME = "recording.mp3" # keep track of the MP3 filename across processes
	TRANSCRIPTION_FILENAME = "transcription.txt" # keep track across processes
	
	logging.info("audio file changed, getting transcription...")
	
	# speech-to-text with Whisper
	audio_file = open(MP3_FILENAME, 'rb')
	transcribe = client.audio.transcriptions.create(model="whisper-1", 
														file=audio_file,
														temperature=0,
														response_format="text")
	current_transcription = str(transcribe)
	
	# save the transcription to a text file
	with open(TRANSCRIPTION_FILENAME, 'a') as f:
		f.write(str(datetime.now())[:19] + " " + current_transcription)
		f.write('\n')
	
	inputs[0] = 0 # tell the main loop that the file has been transcribed
	logging.info("current transcription: " + current_transcription)
	os.remove(MP3_FILENAME) # remove the mp3 recording
	
def brainstorm(inputs):
	TRANSCRIPTION_FILENAME = "transcription.txt" # keep track across processes
	CONCEPTS_FILENAME = "generated_concepts.txt" # keep track across processes

	f = open(TRANSCRIPTION_FILENAME,mode='r')
	transcription = f.read()
	
	output = client.chat.completions.create(
		model="gpt-3.5-turbo",
		messages=[
		{"role": "system", "content": "You are a brainstorming assistant for a meeting room. Your job is to listen in to the conversation that is happening, the sticky notes that are on the whiteboard, and generate concepts that aid in the brainstorming process. The format you should return is each concept separated by commas. Please ONLY RETURN THE CONCEPTS as your output."},
		{"role": "user", "content": "The transcription is: " + transcription},
		{"role": "user", "content": "The sticky notes show: " + str()}
		],
		temperature=0.8 # GPT config - higher temp is more creative
	)
	response = output.choices[0].message.content
	responses = response.split(',') # split by concept
	
	# save the transcription to a text file
	with open(CONCEPTS_FILENAME, 'a') as f:
		f.write(str(datetime.now())[:19] + " ")
		for concept in responses:
			f.write(concept)
			f.write('\n')
	
	logging.info("current concepts: ")
	for concept in responses:
		print(concept)