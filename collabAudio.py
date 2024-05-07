import os
import logging

# list input devices, p = pyAudio instance
def list_input_device(p):
	nDevices = p.get_device_count()
	logging.debug('Found input devices:')
	for i in range(nDevices):
		deviceInfo = p.get_device_info_by_index(i)
		devName = deviceInfo['name']
		logging.debug(f"Device ID {i}: {devName}")

# audio process
def audio(inputs):
	# ALL THESE IMPORTS MUST BE IN THIS FUNCTION FOR PROCESS TO WORK
	import wave
	import pydub
	import pyaudio
	import sounddevice
	
	# recording configuration
	DEVICE = 1
	FORMAT = pyaudio.paInt32
	CHANNELS = 1
	RATE = 44100
	CHUNK = 1024
	RECORD_SECONDS = 10
	OUTPUT_FILENAME = "recording.wav"
	MP3_FILENAME = "recording.mp3" # keep track of the MP3 filename across processes
	
	audioInstance = pyaudio.PyAudio() # initialize audio
	list_input_device(audioInstance)
	logging.info("PyAudio initialized")
	
	for i in range(1):
		try:
			logging.info("recording started...")
			stream = audioInstance.open(format=FORMAT, channels=CHANNELS,
								rate=RATE, input=True, input_device_index=DEVICE,
								frames_per_buffer=CHUNK)
			frames = []
			for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
				data = stream.read(CHUNK)
				frames.append(data)
			
			# stop stream - might prevent PyAudio issues
			stream.stop_stream()
			stream.close()
			logging.info("recording finished.")
		except:
			logging.error("recording failed!")
			continue # jump to beginning of loop so we don't try to use the non-existent recording
		
		# generate .wav file
		with wave.open(OUTPUT_FILENAME, 'wb') as wf:
			wf.setnchannels(CHANNELS)
			wf.setsampwidth(audioInstance.get_sample_size(FORMAT))
			wf.setframerate(RATE)
			wf.writeframes(b''.join(frames))
		
		# convert .wav to .mp3
		mp3 =  pydub.AudioSegment.from_wav(OUTPUT_FILENAME)
		mp3.export(MP3_FILENAME, format="mp3")
		
		os.remove(OUTPUT_FILENAME) # remove the wav recording
		
		inputs[0] = 1 # tell the main loop that the file has been updated
		
		audioInstance.terminate() # terminate audio