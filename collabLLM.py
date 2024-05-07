import os
import logging
from openai import OpenAI
from datetime import datetime
from dotenv import load_dotenv

load_dotenv() # use .env file for API key
client = OpenAI() # initialize AI

def transcribe(inputs):
	# wait for audio recording to finish
	while inputs[0] != 1:
		continue
	
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
	
	inputs[0] = 0 # tell the audio loop that the file has been transcribed
	inputs[1] = 1 # tell the brainstorm loop that the transcription file exists
	logging.info("current transcription: " + current_transcription)
	os.remove(MP3_FILENAME) # remove the mp3 recording
	
def brainstorm(inputs):
	TRANSCRIPTION_FILENAME = "transcription.txt" # keep track across processes
	CONCEPTS_FILENAME = "generated_concepts.txt" # keep track across processes
	STICKIES_FILENAME = "stickies.txt" # to save across processes
	SUMMARY_FILENAME = "summary.txt" # keep track across processes
	IMAGE_FILENAME = "image.txt" # keep track across processes
	
	try:
		os.remove(CONCEPTS_FILENAME) # remove the previous concepts
	except:
		logging.warning("no concepts file")
		
	try:
		os.remove(SUMMARY_FILENAME) # remove the previous concepts
	except:
		logging.warning("no summary file")
	
	# wait for transcription file to show up
	while inputs[1] != 1:
		continue
	
	# wait for stickies to show up
	while inputs[2] != 1:
		continue

	f = open(TRANSCRIPTION_FILENAME,mode='r')
	transcription = f.read()
	
	f = open(STICKIES_FILENAME,mode='r')
	stickies = f.read()
	
	output = client.chat.completions.create(
		model="gpt-3.5-turbo",
		messages=[
		{"role": "system", "content": "You are a brainstorming assistant for a meeting room. Your job is to listen in to the conversation that is happening, the sticky notes that are on the whiteboard, and generate two-word concepts that aid in the brainstorming process. The format you should return is each concept separated by commas. Please ONLY RETURN THE CONCEPTS as your output."},
		{"role": "user", "content": "The transcription is: " + transcription},
		{"role": "user", "content": "The sticky notes show (format is x, y, w, h, text, dist, ignore everything aside from text): " + stickies}
		],
		temperature=0.8 # GPT config - higher temp is more creative
	)
	response = output.choices[0].message.content
	responses = response.split(',') # split by concept
	
	# save the concepts to a text file
	with open(CONCEPTS_FILENAME, 'a') as f:
		# f.write(str(datetime.now())[:19] + " ")
		for concept in responses:
			f.write(concept)
			f.write('\n')
	
	logging.info("current concepts: ")
	for concept in responses:
		print(concept)
		
	output2 = client.chat.completions.create(
		model="gpt-3.5-turbo",
		messages=[
		{"role": "system", "content": "You are a brainstorming assistant for a meeting room. Your job is to listen in to the conversation that is happening, the sticky notes that are on the whiteboard, and generate a concise summary of the brainstorming session, in Ernest Hemingway style. Don't include the sticky notes or their numbers in the summary. Don't return anything aside from the summary."},
		{"role": "user", "content": "The transcription is: " + transcription},
		{"role": "user", "content": "The sticky notes show: " + stickies}
		],
		temperature=0.2 # GPT config - higher temp is more creative
	)
	response2 = output2.choices[0].message.content	
	
	# save the summary to a text file
	with open(SUMMARY_FILENAME, 'a') as f:
		f.write(response2)
	
	output3 = client.chat.completions.create(
		model="gpt-3.5-turbo",
		messages=[
		{"role": "system", "content": "You are a brainstorming assistant for a meeting room. Your job is to listen in to the conversation that is happening, the sticky notes that are on the whiteboard, and generate a DALLE-3 prompt for an image that captures the concept. The sticky notes are in the format 'x, y, w, h, content, distance.' Ignore x, y, w, h. The larger the distance number, the less that sticky note should weigh on the image. The smaller that distance number, the more that particular sticky note should weigh on the image. Only return the prompt and nothing else."},
		{"role": "user", "content": "The transcription is: " + transcription},
		{"role": "user", "content": "The sticky notes show: " + stickies}
		],
		temperature=0.5 # GPT config - higher temp is more creative
	)
	response3 = output3.choices[0].message.content	
	
	response4 = client.images.generate(
	  model="dall-e-3",
	  prompt=response3,
	  size="1024x1024",
	  quality="standard",
	  n=1,
	)
	
	image_url = response4.data[0].url
		
	# save the summary to a text file
	with open(IMAGE_FILENAME, 'a') as f:
		f.write(response3 + "~ " + image_url)
		f.write('\n')
	
	inputs[1] = 0 # tell the transcription loop that the transcription file has been read
	inputs[2] = 0 # tell the stickies loop that the stickies been read