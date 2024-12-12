from moviepy.video.io.VideoFileClip import VideoFileClip
import wave
import numpy as np
import speech_recognition as sr
import json

# Extracting audio from video
def extract_audio(video_path, audio_path):
    # Load the video clip
    video_clip = VideoFileClip(video_path)
    # Extract audio from the video clip
    audio_clip = video_clip.audio
    # Write the audio to a new file
    audio_clip.write_audiofile(audio_path, codec='pcm_s16le') # You can change the codec if needed
    # Close the video clip
    video_clip.close()

# Processing the audio
def process_audio(input_path, output_path):
    # Open the input audio file
    with wave.open(input_path, 'rb') as input_wave:
        # Get audio parameters
        channels = input_wave.getnchannels()
        sample_width = input_wave.getsampwidth()
        frame_rate = input_wave.getframerate()
        frames = input_wave.getnframes()
        # Read audio data
        audio_data = np.frombuffer(input_wave.readframes(frames), dtype=np.int16)
        # Perform audio processing (example: increase volume by 2)
        processed_audio = np.clip(audio_data * 2, -32768, 32767)
    # Open the output audio file
    with wave.open(output_path, 'wb') as output_wave:
        # Set output audio parameters
        output_wave.setnchannels(channels)
        output_wave.setsampwidth(sample_width)
        output_wave.setframerate(frame_rate)
        # Write processed audio data
        output_wave.writeframes(processed_audio.tobytes())

# Extracting the transcript from the processed audio
def extract_transcript(audio_path, language="en-US"):
    # Initialize the recognizer
    recognizer = sr.Recognizer()
    # Load the audio file
    with sr.AudioFile(audio_path) as audio_file:
        # Adjust for ambient noise
        recognizer.adjust_for_ambient_noise(audio_file)
        # Record the audio
        audio = recognizer.record(audio_file)
    try:
        # Use Google Web Speech API to recognize the audio
        transcript = recognizer.recognize_google(audio, language=language)
        return transcript
    except sr.UnknownValueError:
        print("Google Web Speech API could not understand audio")
        return ""
    except sr.RequestError as e:
        print(f"Could not request results from Google Web Speech API; {e}")
        return ""

if __name__ == "__main__":
    video_path = "video2.mp4"
    extracted_audio_path = "extracted.wav"
    processed_audio_path = "processed.wav"
    language = "kn-IN"  # Change this to the desired language code, e.g., "es-ES" for Spanish

    extract_audio(video_path, extracted_audio_path)  # Extracting audio from video.
    process_audio(extracted_audio_path, processed_audio_path)  # Processing the extracted audio.
    transcript = extract_transcript(processed_audio_path, language=language)  # Extracting the transcript from the processed audio.

    # Adding the transcript to a json file.
    with open('transcript_original.json', 'w') as file:
        json.dump(transcript, file)
