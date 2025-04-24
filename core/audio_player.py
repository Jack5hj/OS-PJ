
import pygame

class AudioPlayer:
    def __init__(self):
        pygame.mixer.init()

    def load_song(self, file_path):
        pygame.mixer.music.load(file_path)

    def play(self):
        pygame.mixer.music.play()

    def pause(self):
        pygame.mixer.music.pause()

    def resume(self):
        pygame.mixer.music.unpause()

    def stop(self):
        pygame.mixer.music.stop()
