import pygame
import numpy as np
import librosa
import time
import os

def play_and_visualize(song_path):
   
    y, sr = librosa.load(song_path, sr=None, mono=True)
    total = len(y)
    title = os.path.splitext(os.path.basename(song_path))[0]
    pygame.init()
    screen = pygame.display.set_mode((800, 400))
    pygame.display.set_caption(f"Zhatify Visualizer – {title}")
    clock = pygame.time.Clock()
    N = 1024
    window_fn = np.hanning(N)
    bar_color = (0,255,0)
    top_h = 40
    start = time.time()
    running = True
    while running:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = False
                break

        t = time.time() - start
        idx = int(t * sr)
        if idx >= total:
            break

        if idx < N:
            segment = np.zeros(N)
            segment[N-idx:] = y[:idx]
        else:
            segment = y[idx-N:idx]
        segment *= window_fn

        mags = np.abs(np.fft.rfft(segment))[:50]
        m = mags.max() if mags.size else 0.0
        if m > 0:
            heights = (mags / m) * (400 - top_h)
        else:
            heights = np.zeros_like(mags)
     

        screen.fill((0,0,0))
        pygame.draw.rect(screen, (255,255,255), (0,0,800,top_h))
        font = pygame.font.Font(None, 28)
        txt = font.render(title, True, (0,0,0))
        screen.blit(txt, (10,5))

        w = 800 / len(heights)
        for i, h in enumerate(heights):
            bar_h = int(h) 
            x = int(i * w)
            pygame.draw.rect(screen, bar_color,
                             (x, 400 - bar_h, int(w-2), bar_h))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
