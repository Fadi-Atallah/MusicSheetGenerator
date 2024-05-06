from audioSimilarityCheck import similarityCheck, similarityCheckplot
import mido
from midi2audio import FluidSynth
import random
import matplotlib.pyplot as plt
import librosa
import soundfile as sf


def convert():
    midiFile = "D:/Thesis/MusicSheetGenerator/g.mid"
    soundfont = "D:/Intern/FluidR3_GM.sf2"
    fs = FluidSynth(soundfont)
    mp3File = "D:/Thesis/MusicSheetGenerator/g.wav"
    fs.midi_to_audio(midiFile, mp3File)

def getAudioDetails(audio_file):
    # Load the audio file
    y, sr = librosa.load(audio_file)

    # Find the non-silent intervals
    non_silent_intervals = librosa.effects.split(y, top_db=30)  # Adjust the top_db parameter as needed

    # Extract the non-silent portion of the audio
    trimmed_audio = []
    for interval in non_silent_intervals:
        trimmed_audio.extend(y[interval[0]:interval[1]])

    sf.write("1.wav", trimmed_audio, sr)

    y, sr = librosa.load(audio_file)

    # Calculate onsets
    onset_frames = librosa.onset.onset_detect(y=y, sr=sr)

    # Count the number of onsets
    num_notes = len(onset_frames)
    return num_notes



mid = mido.MidiFile("D:/Thesis/MusicSheetGenerator/1.mid")

similarityValues = []
track = mid.tracks[1]

original_file = "D:/Thesis/MusicSheetGenerator/1.wav"
total_notes = getAudioDetails(original_file)

s = similarityCheckplot(original_file, original_file)
similarityValues.append(s["swass"])

for i in range(0, total_notes):
    index = random.randint(0, total_notes-1)
    if track[index].type == 'note_on':
        track[index].note += 1
    
    mid.save("g.mid")
    convert()
    generated_file = "D:/Thesis/MusicSheetGenerator/g.wav"

    if i == total_notes//2 or i == total_notes-1:
        s = similarityCheckplot(original_file, generated_file)
        similarityValues.append(s["swass"])
    else:
        s = similarityCheck(original_file, generated_file)
        similarityValues.append(s["swass"])

print(similarityValues)
plt.plot(similarityValues)
plt.show()
