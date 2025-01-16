import sounddevice as sd
import wave
import numpy as np
import os

# Ayarlar
Threshold = 30  # Eşik değeri (dB cinsinden)
RATE = 44100  # Örnekleme hızı
CHANNELS = 1  # Stereo kayıt
DURATION = 100  # Maksimum kayıt süresi
FILENAME = "recording.wav"  # Kayıt dosyası adı

def rms(data):
    # Veriyi numpy array'e çevir
    data = np.frombuffer(data, dtype=np.int16)
    return np.sqrt(np.mean(data**2))

def callback(indata, frames, time, status):
    global recording, audio_data
    if status:
        print(status)
    volume_norm = rms(indata) * 1000
    if volume_norm > Threshold:
        print(f"Ses tespit edildi: {volume_norm}")
        recording = True
        audio_data.append(indata.tobytes())
    elif recording:
        print("Kayıt tamamlandı.")
        recording = False

def main():
    global recording, audio_data
    recording = False
    audio_data = []

    input_device = 23  # Stereo Mix cihazının index numarası

    with sd.InputStream(callback=callback, channels=CHANNELS, samplerate=RATE, device=input_device):
        print("Dinlemeye başlandı. Ses tespit edildiğinde kayıt yapılacak...")
        sd.sleep(int(DURATION * 1000))

    if audio_data:
        audio_data = b''.join(audio_data)
        write_wave_file(audio_data, FILENAME)

def write_wave_file(data, filename):
    if os.path.exists(filename):
        os.remove(filename)
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(2)  # 16 bit
        wf.setframerate(RATE)
        wf.writeframes(data)
    print(f"Kayıt {filename} dosyasına kaydedildi.")

if __name__ == "__main__":
    main()
