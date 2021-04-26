import sys
import os

import torch
import librosa
import soundfile as sf
import numpy as np
import tkinter as tk
from tkinter import filedialog
import openunmix
from PySide6 import QtCore


class Main(QtCore.QThread):

    def __init__(self):
        super(Main, self).__init__()
        self.global_objects = {}

    def add_ffmpeg_to_env(self):
        self.global_objects['PATH'] = os.environ['PATH']
        if 'ffmpeg' in self.global_objects['PATH']:
            ffmpeg_path = os.path.dirname(os.path.abspath(__file__))
            ffmpeg_path = os.path.join(ffmpeg_path, 'ffmpeg')
            ffmpeg_path = os.path.join(ffmpeg_path, 'bin')
            os.environ['PATH'] += ';' + ffmpeg_path

    # Input Tensor Shape of (nb_samples, nb_channels, nb_timesteps)
    # Output Tensor Shape of (nb_samples, nb_channels, nb_timesteps)
    def predict(self, wav: torch.Tensor) -> (torch.Tensor, int):
        separator = openunmix.umxhq()
        estimates = separator(wav)
        return estimates[:, 0, :, :].squeeze()

    # Input filename in string
    # Output wav Tensor of shape (nb_samples, nb_channels, nb_timesteps), and sample_rate in int
    def load(self, filename: str) -> torch.Tensor:
        wav, sample_rate = librosa.load(filename, sr=22050, mono=False, dtype=np.float64)
        wav = torch.Tensor(wav)
        if wav.ndim == 1:
            wav = torch.stack([wav, wav])
        wav = wav.reshape((1, wav.shape[0], wav.shape[1]))

        return wav, sample_rate

    # Input path in string, Tensor of shape (nb_channels, nb_timesteps)
    def save(self, path: str, wav: torch.Tensor, sample_rate: int) -> None:
        if not os.path.exists(os.path.dirname(path)):
            os.mkdir(os.path.dirname(path))
        sf.write(path, np.transpose(wav.detach().numpy()), sample_rate)

    def run(self):
        wav, rate = self.load(self.global_objects['filename'])
        wav_out = self.predict(wav)

        filename = os.path.basename(self.global_objects['filename'])
        path = os.path.dirname(self.global_objects['filename'])

        filename = 'extracted_' + filename

        filename, _ = os.path.splitext(filename)
        filename += '.wav'

        path = os.path.join(path, filename)

        self.save(path, wav_out, rate)
