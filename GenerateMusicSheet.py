import librosa
import soundfile as sf
from midi2audio import FluidSynth
from midiutil import MIDIFile
from geneticAlgorithm import geneticAlgorithm
from audioSimilarityCheck import similarityCheck
import random
import os
import copy
import matplotlib.pyplot as plt
import time

def convert():
    midiFile = "D:/Thesis/MusicSheetGenerator/generated.mid"
    soundfont = "D:/Intern/FluidR3_GM.sf2"
    fs = FluidSynth(soundfont)
    wavFile = "D:/Thesis/MusicSheetGenerator/generated.wav"
    fs.midi_to_audio(midiFile, wavFile)

    y, sr = librosa.load(wavFile)
    non_silent_intervals = librosa.effects.split(y, top_db=30)
    trimmed_audio = []
    for interval in non_silent_intervals:
        trimmed_audio.extend(y[interval[0]:interval[1]])

    sf.write(wavFile, trimmed_audio, sr)


def getAudioDetails(audio_file):
    # Load the audio file
    y, sr = librosa.load(audio_file)

    # Find the non-silent intervals
    non_silent_intervals = librosa.effects.split(y, top_db=30) 

    # Extract the non-silent portion of the audio
    trimmed_audio = []
    for interval in non_silent_intervals:
        trimmed_audio.extend(y[interval[0]:interval[1]])

    sf.write(audio_file, trimmed_audio, sr)

    y, sr = librosa.load(audio_file)

    # Calculate onsets
    onset_frames = librosa.onset.onset_detect(y=y, sr=sr)

    # Count the number of onsets
    num_notes = len(onset_frames)
    print("Number of notes:", num_notes)

    # Calculate duration
    duration = librosa.get_duration(y=y, sr=sr)

    num_measures = ((duration / 60) * 100) // 4

    print(num_measures)

    return num_notes, num_measures

def generate_population(num_notes, num_measures):
    population = geneticAlgorithm.generate_population(25, num_notes, num_measures)
    return population


def melody_to_midi(melody):
    mf = MIDIFile(1)
    
    bpm = 100
    track = 0
    channel = 0

    time = 0.0
    mf.addTrackName(track, time, "Sample Track")
    mf.addTempo(track, time, bpm)

    for i, vel in enumerate(melody["velocity"]):
        if vel > 0:
            mf.addNote(track, channel, melody["notes"][i], time, melody["beat"][i], vel)

        time += melody["beat"][i]
    
    filename = "D:/Thesis/MusicSheetGenerator/generated.mid"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "wb") as f:
        mf.writeFile(f)


def fitnessFunction (genom, audio_file):
    melody_to_midi(genom)

    convert()
    generated_file = "D:/Thesis/MusicSheetGenerator/generated.wav"

    fitnessValue = similarityCheck(audio_file, generated_file)
    print(fitnessValue["swass"])
    return fitnessValue["swass"]


    

def main():
    audio_file = 'D:/Thesis/MusicSheetGenerator/1.wav'
    generation = 1
    
    num_notes, num_measures = getAudioDetails(audio_file)
    
    population = generate_population(num_notes, num_measures)
    maxSimilarity = []
    sorted_population_fitness = []
    next_generation = []
    
    while True:
        start_time = time.time()
        print("------------------------------------------------------")
        print("generation: " , generation)
        population_fitness = [(genom, fitnessFunction(genom, audio_file)) for genom in population]
        # print(population_fitness)
        sorted_population_fitness = sorted(population_fitness, key=lambda e: e[1], reverse=True)
        # print(sorted_population_fitness)
        print(sorted_population_fitness[0][1])
        maxSimilarity.append(sorted_population_fitness[0][1])

        if generation % 30 == 0 :
            plt.plot(maxSimilarity)
            plt.show()

        if sorted_population_fitness[0][1] >= 0.98:
            print("found in generation number: " , generation)
            melody_to_midi(sorted_population_fitness[0][0])
            break

        population = [e[0] for e in sorted_population_fitness] 

        
        next_generation.append(copy.deepcopy(population[0]))
        next_generation.append(copy.deepcopy(population[1]))
        parent1 = copy.deepcopy(population[0])
        parent2 = copy.deepcopy(population[1])
        # print(next_generation)
        for _ in range(int(len(population) / 2) - 1):
        
            # print(id(next_generation[0]))
            # print("parent 1 ",id(parent1))
            # print("parent 1 ",parent1)
            offspring_a, offspring_b = geneticAlgorithm.single_point_crossover(parent1, parent2)
            offspring_a = geneticAlgorithm.mutation(parent1, num_measures, num=1)
            # print(next_generation[0])
            # print("parent 1 ",parent1)
            # print(offspring_a)
            offspring_b = geneticAlgorithm.mutation(parent2, num_measures, num=1)
            # print(next_generation[1])
            # print(offspring_b)
            next_generation.append(offspring_a)
            next_generation.append(offspring_b)
        
        population = copy.deepcopy(next_generation)
        next_generation.clear()
        generation += 1
        melody_to_midi(population[0])
        print("Execution time: ", time.time() - start_time)
        input("Press Enter to continue...")


if __name__ == '__main__':
    main()