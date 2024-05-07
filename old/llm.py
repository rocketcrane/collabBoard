import logging
from openai import OpenAI
from dotenv import load_dotenv

# initialize AI
load_dotenv() # use .env file for API key
client = OpenAI()

# global variables to store the transcription and OCR text
transcription = "okay so we're designing a computer mouse but it has to be really different"
stickies = "cheesy, Dole, cool, insane, gamer"

GPT_TEMP = 0.8 # GPT config - higher temp is more creative

logging.basicConfig(level=logging.INFO) # set logging level

output = client.chat.completions.create(
	model="gpt-3.5-turbo",
	messages=[
	{"role": "system", "content": "You are a brainstorming assistant for a meeting room. Your job is to listen in to the conversation that is happening, the sticky notes that are on the whiteboard, and generate concepts that aid in the brainstorming process. The format you should return is each concept separated by commas. Please ONLY RETURN THE CONCEPTS as your output."},
	{"role": "user", "content": "The transcription is: " + str(transcription)},
	{"role": "user", "content": "The sticky notes show: " + str(stickies)}
	],
	temperature=GPT_TEMP
)
response = output.choices[0].message.content

responses = response.split(',')

logging.info(responses)
logging.info(responses[0])
logging.info(responses[1])
logging.info(responses[2])
logging.info(len(responses))

response = client.images.generate(
  model="dall-e-3",
  prompt=responses[2],
  size="1024x1024",
  quality="standard",
  n=1,
)

image_url = response.data[0].url

logging.info(image_url)