from midi2audio import FluidSynth

soundfont = "D:/Intern/FluidR3_GM.sf2"
fs = FluidSynth(soundfont)
midiFile = "D:/Thesis/New folder/1.mid"
mp3File = "D:/Thesis/New folder/1.wav"
fs.midi_to_audio(midiFile, mp3File)