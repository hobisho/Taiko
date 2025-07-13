import librosa

def find_bpm(file_path):
    # Load the audio file
    y, sr = librosa.load(file_path)

    # Estimate the tempo (BPM)
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)

    return tempo

if __name__ == "__main__":
    file_path = input("Enter the path to the audio file: ")
    bpm = find_bpm(file_path)
    print(f"The estimated BPM of the song is: {bpm}")