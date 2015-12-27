#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import json
from sys import byteorder
from array import array
# from struct import pack
import numpy
import pyaudio
import wave

class AudioRecord(object):
    def __init__(
        self,
        threshold=700,
        chunk_size=512, #1024,
        format=pyaudio.paInt16,
        rate=44100
    ):
        self.threshold = threshold
        self.chunk_size = chunk_size
        self.format = format
        self.rate = rate
        self.portaudio = pyaudio.PyAudio()
        self.input_device_index = 0
        self.output_device_index = 0

    def get_devices(self):
        devices = []
        for idx in range(self.portaudio.get_device_count()):
            devices.append(self.portaudio.get_device_info_by_index(idx))
        return devices

    def set_input_device_index(self, idx):
        self.input_device_index = idx

    def set_output_device_index(self, idx):
        self.output_device_index = idx

    def is_silent(self, snd_data):
        return max(snd_data) < self.threshold

    def normalize(self, snd_data):
        MAXIMUM = 16384
        times = float(MAXIMUM)/max(abs(i) for i in snd_data)

        r = array('h')
        for i in snd_data:
            r.append(int(i*times))
        return r

    def record(self):
        p = pyaudio.PyAudio()

        device_info = self.portaudio.get_device_info_by_index(
            self.input_device_index
        )
        stream = p.open(
            format=self.format,
            channels=device_info['maxInputChannels'],
            rate=int(device_info['defaultSampleRate']),
            input=True,
            frames_per_buffer=self.chunk_size,
            input_device_index=self.input_device_index
        )

        num_silent = 0
        snd_started = False#True

        r = array('h')

        while 1:
            # little endian, signed short
            buf = stream.read(self.chunk_size)
            # print "buf size: ", len(buf)
            snd_data = array('h', buf)
            # print "snd_data size: ", len(snd_data)
            if byteorder == 'big':
                snd_data.byteswap()
            if snd_started:
            	r.extend(snd_data)

            silent = self.is_silent(snd_data)

            if silent and snd_started:
                # print "silent"
                num_silent += 1
            elif not silent and not snd_started:
                snd_started = True
                print "record start"
            	print max(snd_data)

            if snd_started and num_silent > 60:
                print "record end"
                break

        print "array size: ", len(r)
        sample_width = p.get_sample_size(self.format)
        stream.stop_stream()
        stream.close()
        p.terminate()

        # r = self.normalize(r)
        return sample_width, r

    def record_to_file(self, path, microcone=True):

        sample_width, data = self.record()
        ary = numpy.frombuffer(data, dtype=numpy.int16)

        if microcone:
            ## converting 8 channel to 7 channel
            ary.shape = 8, ary.shape[0] / 8
            ary = ary[0:7, :]
            ary.shape = ary.shape[0] * ary.shape[1],
            input_channel = 7
        else:
            device_info = self.portaudio.get_device_info_by_index(
                self.input_device_index
            )
            input_channel = device_info['maxInputChannels']

        # print "recording 7 channel data ..."
        wf = wave.open(path, 'wb')
        wf.setnchannels(input_channel)
        wf.setsampwidth(sample_width)
        wf.setframerate(self.rate)
        wf.writeframes(array('h', ary).tostring())
        wf.close()


if __name__ == '__main__':
    import argparse
    from pprint import pprint

    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument('-s', '--segment_threshold', type=int, default=700)
    parser.add_argument('-n', '--num_sources', type=int, default=2)
    args = parser.parse_args()

    m = AudioRecord(threshold=args.segment_threshold)
    keyword="hw:1,0"
    print "*****"
    device_index = -1
    microcone = False
    for idx, entry in enumerate(m.get_devices()):
        if entry['name'].find(keyword) >= 0:
            device_index = idx
            pprint('>>>[{}] {}'.format(idx, entry))
            break
    if device_index < 0:
        print "failed to find keyword..."
        sys.exit(1)
    m.set_input_device_index(device_index)
    print device_index
    print "start recording ..."
    m.record_to_file('rec.wav', microcone=microcone)
    print("result written to rec.wav")

    

