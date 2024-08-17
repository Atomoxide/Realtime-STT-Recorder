# import required libraries
import sounddevice as sd
import scipy.io.wavfile as wavfile
import wavio as wv
import numpy as np
import time
import asyncio
import os
from stt_api import upload_file_async

THRESHOLD = 1.0
FS = 44100
CHAN = 1
STOP_DELAY = 2.0
GAIN_FACTOR = 1.5
URL = "http://127.0.0.1:9977/api"

class Record():
    
    def __init__(self):
        self.is_recording = False
        self.recoding_sequence = list()
        self.stop_timer = None
        self.amplified_data = list()
        self.loop = asyncio.get_event_loop()
        

    def audio_callback(self, indata, frames, callback_time, status):
        volume_norm = np.linalg.norm(indata)*10
        current_time = time.monotonic()
        
        if volume_norm > THRESHOLD:
            if not self.is_recording:
                print("start recording")
                self.is_recording = True
                self.stop_timer = None
            else:
                self.stop_timer = current_time
        elif self.is_recording:
            if self.stop_timer is None:
                self.stop_timer = current_time
            if current_time - self.stop_timer >= STOP_DELAY:
                print("stop recording")
                self.is_recording = False
                
                # Amplify the recording data by the gain factor
                self.amplified_data = np.concatenate(self.recoding_sequence, axis=0) * GAIN_FACTOR
                
                # Clip the data to avoid overflow issues
                self.amplified_data = np.clip(self.amplified_data, -1.0, 1.0)
            
                if self.recoding_sequence:
                    wav_filename = f'./outputs/recording_{str(int(time.monotonic()))}.wav'
                    wavfile.write(wav_filename, FS, np.concatenate(self.amplified_data, axis=0))
                    print(f"Saved {wav_filename}")
                    self.recoding_sequence = list()
                    asyncio.run_coroutine_threadsafe(upload_file_async(wav_filename), self.loop)
                            
        if self.is_recording:
            self.recoding_sequence.append(indata.copy())
                

if __name__ == "__main__":
    record = Record()

    with sd.InputStream(callback=record.audio_callback, channels=CHAN, samplerate=FS):
        try:
            while True:
                # time.sleep(1)
                record.loop.run_forever()
                # pass
        except KeyboardInterrupt:
            print("\nRecording finished.")
            record.loop.run_until_complete(asyncio.sleep(0))
            record.loop.stop()
            record.loop.close()



