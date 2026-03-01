import pygame
import math
import array


def _generate_wave(frequency, duration_ms, volume=0.3, wave_type="sine"):
    """Gera uma onda sonora como pygame.mixer.Sound."""
    sample_rate = 44100
    n_samples = int(sample_rate * duration_ms / 1000)

    samples = array.array("h")  # signed short (16-bit)

    for i in range(n_samples):
        t = i / sample_rate
        # Envelope (fade in/out)
        env = 1.0
        fade = int(n_samples * 0.1)
        if i < fade:
            env = i / fade
        elif i > n_samples - fade:
            env = (n_samples - i) / fade

        if wave_type == "sine":
            val = math.sin(2 * math.pi * frequency * t)
        elif wave_type == "square":
            val = 1.0 if math.sin(2 * math.pi * frequency * t) > 0 else -1.0
        else:
            val = math.sin(2 * math.pi * frequency * t)

        sample = int(val * volume * 32767 * env)
        sample = max(-32767, min(32767, sample))
        samples.append(sample)

    sound = pygame.mixer.Sound(buffer=samples)
    return sound


def _generate_multi_tone(tones, volume=0.3):
    """Gera som com múltiplas notas em sequência.
    tones: lista de (frequência, duração_ms)
    """
    sample_rate = 44100
    samples = array.array("h")

    for freq, dur_ms in tones:
        n = int(sample_rate * dur_ms / 1000)
        for i in range(n):
            t = i / sample_rate
            env = 1.0
            fade = int(n * 0.15)
            if i < fade:
                env = i / fade
            elif i > n - fade:
                env = (n - i) / fade

            val = math.sin(2 * math.pi * freq * t)
            sample = int(val * volume * 32767 * env)
            samples.append(max(-32767, min(32767, sample)))

    return pygame.mixer.Sound(buffer=samples)


def generate_eat_sound():
    """Som de comer fruta: blip agudo e curto."""
    return _generate_multi_tone([
        (880, 50),
        (1100, 60),
    ], volume=0.25)


def generate_special_sound():
    """Som de fruta especial: arpejo ascendente."""
    return _generate_multi_tone([
        (523, 60),   # C
        (659, 60),   # E
        (784, 60),   # G
        (1047, 80),  # C oitava acima
    ], volume=0.25)


def generate_gameover_sound():
    """Som de game over: descida grave."""
    return _generate_multi_tone([
        (400, 150),
        (300, 150),
        (200, 200),
        (150, 300),
    ], volume=0.3)


class SoundManager:
    def __init__(self):
        self.enabled = True
        try:
            self.eat = generate_eat_sound()
            self.special = generate_special_sound()
            self.gameover = generate_gameover_sound()
        except Exception:
            self.enabled = False

    def play_eat(self):
        if self.enabled:
            self.eat.play()

    def play_special(self):
        if self.enabled:
            self.special.play()

    def play_gameover(self):
        if self.enabled:
            self.gameover.play()
