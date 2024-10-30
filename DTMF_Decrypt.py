# © KahlerYasla on GitHub

import numpy as np
import wave
import os

# DTMF Frequency
DTMF_FREQS = {
    '1': (20697, 21209),
    '2': (20697, 21336),
    '3': (20697, 21477),
    '4': (20770, 21209),
    '5': (20770, 21336),
    '6': (20770, 21477),
    '7': (20852, 21209),
    '8': (20852, 21336),
    '9': (20852, 21477),
    '0': (20941, 21336),
    '*': (20941, 21209),
    '#': (20941, 21477)
}
# ------------------------------------------------------------------------------
def decode_dtmf(sig, Fs, window=0.05, ofset=10):
    # Initialize empty list to store the decoded keys and frequencies found
    keys = []
    found_freqs = []

    # Iterate through the signal in window-sized chunks
    for i in range(0, len(sig), int(Fs * window)):
        # Get the current chunk of the signal
        cut_sig = sig[i:i + int(Fs * window)]

        # Take the Fast Fourier Transform (FFT) of the current chunk
        fft_sig = np.fft.fft(cut_sig, Fs)

        # Take the absolute value of the FFT
        fft_sig = np.abs(fft_sig)

        # Set the first 500 elements of the FFT to 0 (removes DC component)
        fft_sig[:500] = 0

        # Only keep the first half of the FFT (removes negative frequencies)
        fft_sig = fft_sig[:int(len(fft_sig) / 2)]

        # Set the lower bound to be 75% of the maximum value in the FFT
        lower_bound = 0.75 * np.max(fft_sig)

        # Initialize empty list to store the frequencies that pass the lower bound threshold
        filtered_freqs = []

        # Iterate through the FFT and store the indices of the frequencies that pass the lower bound threshold
        for i, mag in enumerate(fft_sig):
            if mag > lower_bound:
                filtered_freqs.append(i)

        # Iterate through the DTMF frequencies and check if any of the filtered frequencies fall within the expected range
        for char, frequency_pair in DTMF_FREQS.items():
            high_freq_range = range(frequency_pair[0] - ofset, frequency_pair[0] + ofset + 1)
            low_freq_range = range(frequency_pair[1] - ofset, frequency_pair[1] + ofset + 1)
            if any(freq in high_freq_range for freq in filtered_freqs) and any(
                    freq in low_freq_range for freq in filtered_freqs):
                # If a match is found, append the key and frequency pair to the lists
                keys.append(char)
                found_freqs.append(frequency_pair)

    # Return the decoded keys and found frequencies
    return keys, found_freqs

# ------------------------------------------------------------------------------
def analyze_audio(filename):
    # Open the audio file
    wave_file = wave.open(filename, 'r')
    num_samples = wave_file.getnframes()
    Fs = wave_file.getframerate()
    data = wave_file.readframes(num_samples)
    sample_width = wave_file.getsampwidth()

    if sample_width == 1:
        data = np.frombuffer(data, dtype=np.int8)
    elif sample_width == 2:
        data = np.frombuffer(data, dtype=np.int16)

        wave_file.close()

        # Decode the DTMF tones
        keys, found_freqs = decode_dtmf(data, Fs, duration + silence_duration)

        # Convert the list of keys to a string
        key_string = ''.join(keys)
        # Return the detected key
        return key_string
# ------------------------------------------------------------------------------
def convert_to_text(key_string):
    num_str = key_string
    text = ""
    for i in range(0, len(num_str), 2):
        # To determine first two digits decimal in keys
        if i + 1 < len(num_str):
            two_digits = int(num_str[i:i + 2])
            # Alphabet A-Z in decimal start from 65-90
            if 65 <= two_digits <= 90:
                text += chr(two_digits)
            # Spacebar (" ") in decimal is 32
            elif two_digits == 32:
                text += chr(two_digits)
            # Eliminate other decimal to ASCII Character convert
            else:
                text += "Invalid input"
        else:
            text += num_str[i]

    #print(text)
    return text
# ------------------------------------------------------------------------------
def vigenere_decrypt(ciphertext, key):
    plaintext = ""
    key_index = 0
    for c in ciphertext:
        if c.isalpha():
            key_char = key[key_index % len(key)]
            key_index += 1
            shift = ord(key_char.upper()) - ord('A')
            if c.isupper():
                plaintext += chr((ord(c) - shift - 65) % 26 + 65)
            else:
                plaintext += chr((ord(c) - shift - 97) % 26 + 97)
        else:
            plaintext += c
    return plaintext
# ------------------------------------------------------------------------------
def get_wav_path():
    while True:
        wav_path = input("Enter the path to the wav file: ")
        if os.path.isfile(wav_path):
            return wav_path
        else:
            print("Invalid file path. Please try again.")
# ------------------------------------------------------------------------------
# Set the sampling frequency (Fs) in Hz
Fs = 441000

# Set the duration of each DTMF tone in seconds
duration = 0.25

# Set the duration of silence between tones in seconds
silence_duration = 0.5

# Get wav path from specific location
wav_path = get_wav_path()

# Analyze the DTMF Signal on wav Audio file
key_string = analyze_audio(wav_path)

# Convert detected DTMF Decimal into codetext
ciphertext = convert_to_text(key_string)

# Input key to decrypt the codetext into plaintext
key = input("Enter the key: ")

# Decrypt codetext using key with vigenere algorithm
plaintext = vigenere_decrypt(ciphertext, key)

# Display the output
print("")
print("ASCII : ", key_string)
print("Text : ", plaintext)
