import numpy as np
from PIL import Image
from scipy.io.wavfile import write
import hashlib

def generate_audio_from_image(image_path, output_path, sample_rate=44100):
    duration_per_col = 0.12
    pixels_per_tone = 8

    C_major_pent = np.array([261.63, 293.66, 329.63, 392.00, 440.00, 523.25])
    C_minor_pent = np.array([261.63, 311.13, 349.23, 392.00, 466.16, 523.25])
    hirajoshi = np.array([261.63, 293.66, 311.13, 392.00, 415.30, 523.25])
    blues = np.array([261.63, 311.13, 349.23, 369.99, 392.00, 466.16, 523.25])
    scales_list = [C_major_pent, C_minor_pent, hirajoshi, blues]

    octave_offsets = {'R': -1, 'G': 0, 'B': 1}
    color_weights = {'R': 0.5, 'G': 0.8, 'B': 0.6}

    img = Image.open(image_path).resize((128, 128))
    pixels = np.array(img) / 255.0
    t_col = np.linspace(0, duration_per_col, int(sample_rate * duration_per_col), endpoint=False)

    img_hash = int(hashlib.sha256(img.tobytes()).hexdigest(), 16)
    rng = np.random.default_rng(img_hash)
    selected_scale = scales_list[img_hash % len(scales_list)]

    sound = np.array([], dtype=np.float32)

    for col in pixels.transpose(1,0,2):
        col = col[::pixels_per_tone]
        r, g, b = col[:,0], col[:,1], col[:,2]

        def brightness_to_freq(channel, octave_offset):
            idx = (channel * (len(selected_scale)-1)).astype(int)
            return selected_scale[idx] * (2**octave_offset)

        freqs_r = brightness_to_freq(r, octave_offsets['R'])
        freqs_g = brightness_to_freq(g, octave_offsets['G'])
        freqs_b = brightness_to_freq(b, octave_offsets['B'])

        phases_r = rng.uniform(0, 2*np.pi, len(r))
        phases_g = rng.uniform(0, 2*np.pi, len(g))
        phases_b = rng.uniform(0, 2*np.pi, len(b))

        envelope = np.sin(np.linspace(0, np.pi, len(t_col)))**2

        tone_r = sum((np.sin(2*np.pi*f*t_col + p) + 0.3*np.sin(2*np.pi*2*f*t_col + p)) * a
                     for f,a,p in zip(freqs_r,r,phases_r)) * envelope * color_weights['R']
        tone_g = sum((np.sin(2*np.pi*f*t_col + p) + 0.3*np.sin(2*np.pi*2*f*t_col + p)) * a
                     for f,a,p in zip(freqs_g,g,phases_g)) * envelope * color_weights['G']
        tone_b = sum((np.sin(2*np.pi*f*t_col + p) + 0.3*np.sin(2*np.pi*2*f*t_col + p)) * a
                     for f,a,p in zip(freqs_b,b,phases_b)) * envelope * color_weights['B']

        tone = tone_r + tone_g + tone_b
        tone /= np.max(np.abs(tone) + 1e-9)
        sound = np.concatenate((sound, tone))

    total_samples = len(sound)
    t_total = np.linspace(0, total_samples/sample_rate, total_samples, endpoint=False)

    drone_rng = np.random.default_rng(img_hash)
    base_drone_freq = drone_rng.uniform(40, 70)
    lfo_amp = drone_rng.uniform(5, 15)
    lfo_rate = drone_rng.uniform(0.01, 0.05)

    lfo = np.sin(2*np.pi*lfo_rate*t_total)
    base_tone = np.sin(2*np.pi*(base_drone_freq + lfo_amp*lfo)*t_total) \
               + 0.5*np.sin(2*np.pi*2*(base_drone_freq + lfo_amp*lfo)*t_total)

    sound += 0.3 * base_tone
    sound /= np.max(np.abs(sound))
    sound_int16 = (sound * 32767).astype(np.int16)

    write(output_path, sample_rate, sound_int16)
    return output_path
