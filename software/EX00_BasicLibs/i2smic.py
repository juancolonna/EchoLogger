import os
import time
from machine import Pin, I2S, SDCard, SoftI2C, ADC, Timer
from bme680 import *


class Controller:
    state="STOP" #"RECORD":0,"PAUSE":1,"RESUME":2,"STOP":3 #chunk_size=2660000  #1min
    base_path=None
    file_path=None
    file_length=0
    record_timer=Timer(0)

    def __init__(self, sck=32, ws=25, sd=33, i2s_id=0, buffer_length=40000, sample_rate=22050, sample_bits=16, chunk_size=2660000):
        self.channels=1        
        self.sample_size = sample_bits // 8
        self.sample_rate=sample_rate
        self.sample_bits=sample_bits
        self.chunk_size=chunk_size
        self.file_counter = 0
        self.audio_in = I2S(
            i2s_id,
            sck=Pin(sck),
            ws=Pin(ws),
            sd=Pin(sd),
            mode=I2S.RX,
            bits=sample_bits,
            format=I2S.MONO,
            rate=sample_rate,
            ibuf=buffer_length,
        )

    def create_wav_header(self,sampleRate, bitsPerSample, num_samples):
        datasize = num_samples * self.channels * bitsPerSample // 8
        o = bytes("RIFF", "ascii")  # (4byte) Marks file as RIFF
        o += (datasize + 36).to_bytes(
            4, "little"
        )  # (4byte) File size in bytes excluding this and RIFF marker
        o += bytes("WAVE", "ascii")  # (4byte) File type
        o += bytes("fmt ", "ascii")  # (4byte) Format Chunk Marker
        o += (16).to_bytes(4, "little")  # (4byte) Length of above format data
        o += (1).to_bytes(2, "little")  # (2byte) Format type (1 - PCM)
        o += (self.channels).to_bytes(2, "little")  # (2byte)
        o += (sampleRate).to_bytes(4, "little")  # (4byte)
        o += (sampleRate * self.channels * bitsPerSample // 8).to_bytes(4, "little")  # (4byte)
        o += (self.channels * bitsPerSample // 8).to_bytes(2, "little")  # (2byte)
        o += (bitsPerSample).to_bytes(2, "little")  # (2byte)
        o += bytes("data", "ascii")  # (4byte) Data Chunk Marker
        o += (datasize).to_bytes(4, "little")  # (4byte) Data size in bytes
        return o
            
    def i2s_callback_rx(self, args):
        if self.state == "RECORD":
            if self.file_length >= self.chunk_size:
                self.audio_in.irq(None)
                self.create_new_file()
            else:
                num_bytes_written = self.file_path.write(self.mic_samples_mv[:self.file_length])
                self.file_length += num_bytes_written
                self.num_read = self.audio_in.readinto(self.mic_samples_mv)                
        elif self.state == "PAUSE":
            time.sleep(0.1)
        else:
            print("Recording done!")
            self.file_path.close()
            self.audio_in.deinit()
    
    def create_new_file(self, first=False):
        self.state="PAUSE"
        if not first: 
            print("Chunk saved!")
            self.file_path.close()
            time.sleep(0.2)

        self.file_counter += 1
        new_filepath = self.base_path+"_{}.wav".format(self.file_counter)
        
        print("Creating new chunk", new_filepath)
        self.file_path = open(new_filepath, "wb")

        #write fix size header
        wav_header = self.create_wav_header(self.sample_rate,self.sample_bits,self.chunk_size // ((self.sample_bits//8) * self.channels))
        num_bytes_written = self.file_path.write(wav_header)
        self.audio_in.irq(self.i2s_callback_rx)
        self.mic_samples = bytearray(10000)
        self.mic_samples_mv = memoryview(self.mic_samples)
        self.file_length = 0
        self.file_length = self.audio_in.readinto(self.mic_samples_mv)
        self.state = "RECORD"
        
    def record(self, filepath):
        self.base_path=filepath
        self.create_new_file(first=True)

    def stop(self): self.state="STOP"
