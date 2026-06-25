"""Audio and visual alert system for bad posture."""

import time
import threading
import pygame


class AlertSystem:
    def __init__(self):
        self._last_alert = 0.0
        self._cooldown = 5.0
        self._init_audio()

    def _init_audio(self):
        try:
            pygame.mixer.init(frequency=22050, size=-16, channels=1)
            self._beep = pygame.mixer.Sound(buffer=self._generate_beep())
        except Exception:
            self._beep = None

    def _generate_beep(self):
        import numpy as np
        sample_rate = 22050
        duration = 0.2
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        wave = np.sin(2 * np.pi * 880 * t) * 0.3
        return (wave * 32767).astype(np.int16).tobytes()

    def trigger(self):
        now = time.time()
        if now - self._last_alert > self._cooldown:
            self._last_alert = now
            if self._beep:
                threading.Thread(target=self._beep.play, daemon=True).start()
