from audio_similarity import AudioSimilarity
import matplotlib.pyplot as plt
import librosa
import soundfile as sf

def similarityCheck(original_audio, compare_audio):

    y, sr = librosa.load(compare_audio)
    non_silent_intervals = librosa.effects.split(y, top_db=30)
    trimmed_audio = []
    for interval in non_silent_intervals:
        trimmed_audio.extend(y[interval[0]:interval[1]])

    sf.write(compare_audio, trimmed_audio, sr)

    sample_rate = 44100

    weights_dict = {
        'zcr_similarity': 0.2,
        'rhythm_similarity': 0.3,
        'chroma_similarity': 0.3,
        'spectral_contrast_similarity': 0.2,
        'perceptual_similarity': 0.0
    }

    audio_similarity = AudioSimilarity(original_audio, compare_audio, sample_rate, weights_dict)

    metrics = {
        #'zcr_similarity': audio_similarity.zcr_similarity(),
        #'rhythm_similarity': audio_similarity.rhythm_similarity(),
        #'chroma_similarity': audio_similarity.chroma_similarity(),
        #'perceptual_similarity': audio_similarity.perceptual_similarity(),
        #'spectral_contrast_similarity': audio_similarity.spectral_contrast_similarity(),
        'stent_weighted_audio_similarity': audio_similarity.stent_weighted_audio_similarity("all")
    }

    return metrics['stent_weighted_audio_similarity']


def similarityCheckplot(original_audio, compare_audio):

    y, sr = librosa.load(compare_audio)
    non_silent_intervals = librosa.effects.split(y, top_db=30)
    trimmed_audio = []
    for interval in non_silent_intervals:
        trimmed_audio.extend(y[interval[0]:interval[1]])

    sf.write(compare_audio, trimmed_audio, sr)

    sample_rate = 44100

    weights_dict = {
        'zcr_similarity': 0.2,
        'rhythm_similarity': 0.3,
        'chroma_similarity': 0.3,
        'spectral_contrast_similarity': 0.2,
        'perceptual_similarity': 0.0
    }

    audio_similarity = AudioSimilarity(original_audio, compare_audio, sample_rate, weights_dict)

    plt.figure(figsize=(9,7))
    plt.subplot(211)
    plt.plot(audio_similarity.original_audios[0])
    plt.xlabel("Original wav file")

    plt.subplot(212)
    plt.plot(audio_similarity.compare_audios[0])
    plt.xlabel("Different wav file")

    plt.show()
    metrics = {
        #'zcr_similarity': audio_similarity.zcr_similarity(),
        #'rhythm_similarity': audio_similarity.rhythm_similarity(),
        #'chroma_similarity': audio_similarity.chroma_similarity(),
        #'perceptual_similarity': audio_similarity.perceptual_similarity(),
        #'spectral_contrast_similarity': audio_similarity.spectral_contrast_similarity(),
        'stent_weighted_audio_similarity': audio_similarity.stent_weighted_audio_similarity("all")
    }

    for metric_name, metric_value in metrics.items():
        print(f"{metric_name}: {metric_value}")

    # Plot with a spider or bar chart
        
    audio_similarity.plot(metrics=['zcr_similarity', 'rhythm_similarity', 'chroma_similarity', 'spectral_contrast_similarity', 'perceptual_similarity'],option='radar',figsize=(8, 6),color1='red',alpha=0.5, title='Audio Similarity Metrics')
    return metrics['stent_weighted_audio_similarity']