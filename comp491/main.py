import tensorflow_hub as hub
import numpy as np
import librosa
import pandas as pd
import urllib.request

# Load the YAMNet model
yamnet_model = hub.load("https://tfhub.dev/google/yamnet/1")

# Download and load the class map
CLASS_MAP_URL = "https://raw.githubusercontent.com/tensorflow/models/master/research/audioset/yamnet/yamnet_class_map.csv"
urllib.request.urlretrieve(CLASS_MAP_URL, "yamnet_class_map.csv")

def load_class_map(file_path="yamnet_class_map.csv"):
    class_map = pd.read_csv(file_path)
    return class_map

class_map = load_class_map()

# Preprocess the audio
def preprocess_audio(file_path):
    audio, sr = librosa.load(file_path, sr=16000)  # Resample to 16kHz
    return audio

# Classify audio using YAMNet
def classify_audio_yamnet(file_path):
    audio = preprocess_audio(file_path)
    waveform = np.array(audio, dtype=np.float32)
    scores, embeddings, spectrogram = yamnet_model(waveform)
    mean_scores = np.mean(scores, axis=0)
    return mean_scores

# Detect human voice
def detect_human_voice(file_path, threshold=0.2):
    mean_scores = classify_audio_yamnet(file_path)
    human_labels = ["Speech", "Conversation", "Singing"]
    human_label_indices = [i for i, label in enumerate(class_map["display_name"]) if label in human_labels]
    human_scores = mean_scores[human_label_indices]
    human_voice_detected = any(score > threshold for score in human_scores)
    for i in human_label_indices:
        print(f"{class_map['display_name'][i]}: {mean_scores[i]:.3f}")
    return "Human Voice" if human_voice_detected else "No Human Voice"

# Main
if __name__ == "__main__":
    file_path = "example.wav"  
    result = detect_human_voice(file_path)
    print(f"Prediction: {result}")



