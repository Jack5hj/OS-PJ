import multiprocessing
import threading
from core.audio_player import AudioPlayer
from playlist.playlist import Playlist
from visuals.live_visualizer import play_and_visualize
from memory_manager.memory import MemoryManager

def main():

    manager  = MemoryManager(capacity=3, swap_enabled=True)
    playlist = Playlist()
    for track in [
        "data/Blank Space.mp3",
        "data/Don't Say.mp3",
        "data/New Romantics.mp3",
        "data/Style.mp3",
        "data/Wildest Dreams.mp3",
        "data/willow.mp3"
    ]:
        playlist.add(track)

    player = AudioPlayer()
    visual_proc = None

    def play_current_song():
        nonlocal visual_proc
        song = playlist.current()
        print(f"\n▶️ Now Playing: {song.split('/')[-1]}")

        manager.load_segment(song, lambda p: open(p, "rb").read())

        player.load_song(song)
        threading.Thread(target=player.play, daemon=True).start()


        if visual_proc and visual_proc.is_alive():
            visual_proc.terminate()
            visual_proc.join()

  
        visual_proc = multiprocessing.Process(
            target=play_and_visualize,
            args=(song,),
            daemon=True
        )
        visual_proc.start()

   
    play_current_song()

   
    while True:
        print("\nCommands: [b] prev | [n] next | [p] pause | [r] resume | [s] stop | [q] quit")
        try:
            cmd = input(">>> ").strip().lower()
        except KeyboardInterrupt:
            print("\n👋 Interrupted—exiting.")
            if visual_proc and visual_proc.is_alive():
                visual_proc.terminate()
            break

        if cmd == 'b':
            player.stop()
            playlist.previous()
            play_current_song()

        elif cmd == 'n':
            player.stop()
            playlist.next()
            play_current_song()

        elif cmd == 'p':
            player.pause()
            print("⏸️ Pausing")

        elif cmd == 'r':
            player.resume()
            print("▶️ Resuming")

        elif cmd == 's':
            player.stop()
            print("⏹️ Stopped")

        elif cmd == 'q':
            player.stop()
            print("👋 Goodbye!")
            if visual_proc and visual_proc.is_alive():
                visual_proc.terminate()
            break

        else:
            print("❓ Unknown command.")

if __name__ == '__main__':
    
    multiprocessing.freeze_support()
    main()
