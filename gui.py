from core.audio_player import AudioPlayer
from playlist.playlist import Playlist
from memory_manager.memory import MemoryManager
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
import librosa

class MusicGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("ZHATIFY")

        
        self.player = AudioPlayer()
        self.strategy_var = tk.StringVar(value="fifo")
        self.memory = MemoryManager(
            capacity=3,
            swap_enabled=True,
            log_callback=self.append_log,
            policy=self.strategy_var.get()
        )

      
        self.playlist = Playlist()
        for song in [
            "data/Blank Space.mp3",
            "data/Don't Say.mp3",
            "data/New Romantics.mp3",
            "data/Style.mp3",
            "data/Wildest Dreams.mp3",
            "data/willow.mp3"
        ]:
            self.playlist.add(song)

      
        self.song_label = tk.Label(master, text="Ready", font=("Arial", 14))
        self.song_label.pack(pady=10)

       
        btn_frame = tk.Frame(master)
        btn_frame.pack(pady=5)
        tk.Button(btn_frame, text="⏮ Prev",    width=8, command=self.previous_song).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="▶ Play",    width=8, command=self.play       ).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="⏸ Pause",   width=8, command=self.pause      ).grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="▶ Resume",  width=8, command=self.resume     ).grid(row=0, column=3, padx=5)
        tk.Button(btn_frame, text="⏭ Next",    width=8, command=self.next_song  ).grid(row=0, column=4, padx=5)
        tk.Button(master,    text="⏹ Stop",    width=8, command=self.stop       ).pack(pady=4)
        tk.Button(master,    text="❌ Exit",    width=8, command=self.exit       ).pack(pady=4)

     
        policy_frame = tk.Frame(master)
        policy_frame.pack(pady=5)
        tk.Label(policy_frame, text="Swap Policy:").pack(side=tk.LEFT)
        tk.OptionMenu(policy_frame,
                      self.strategy_var,
                      "fifo", "smart",
                      command=self.change_strategy).pack(side=tk.LEFT)

   
        list_frame = tk.Frame(master)
        list_frame.pack(pady=5, fill="x")
        tk.Label(list_frame, text="Playlist:").pack(anchor="w")
        self.listbox = tk.Listbox(list_frame, height=6)
        self.listbox.pack(side="left", fill="x", expand=True)
        scrollbar = tk.Scrollbar(list_frame, orient="vertical", command=self.listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.listbox.config(yscrollcommand=scrollbar.set)
 
        for idx, path in enumerate(self.playlist.songs):
            name = path.split("/")[-1]
            self.listbox.insert("end", name)
        self.listbox.select_set(0) 
        self.listbox.bind("<<ListboxSelect>>", self.on_list_select)
        self.current_index = 0


        self.log_box = tk.Text(master, height=8, bg="black", fg="lime", font=("Courier", 10))
        self.log_box.pack(pady=5, fill="x")

        
        self.after_id = None

        self.update_song_label()

    def append_log(self, msg):
        self.log_box.insert(tk.END, msg + "\n")
        self.log_box.see(tk.END)

    def change_strategy(self, value):
        self.memory.policy = value
        self.append_log(f"🔄 Policy switched to: {value.upper()}")

    def on_list_select(self, event):
        sel = event.widget.curselection()
        if not sel:
            return
        idx = sel[0]
        self.current_index = idx
        self.playlist.current_index = idx
        self.play()

    def update_song_label(self):
        song = self.playlist.current()
        self.song_label.config(text=f"🎶 Now Playing: {song.split('/')[-1]}")

    def play(self):
        current = self.playlist.current()
        self.memory.load_segment(current, lambda p: open(p, "rb").read())
        self.player.load_song(current)
        self.player.play()
        self.update_song_label()
        self.show_live_visual(current)

    def pause(self):
        self.player.pause()

    def resume(self):
        self.player.resume()

    def stop(self):
        self.player.stop()
       
        if self.after_id:
            self.master.after_cancel(self.after_id)
            self.after_id = None

    def next_song(self):
        self.player.stop()
        self.playlist.next()
        self.listbox.select_clear(0, "end")
        self.listbox.select_set(self.playlist.current_index)
        self.play()

    def previous_song(self):
        self.player.stop()
        self.playlist.previous()
        self.listbox.select_clear(0, "end")
        self.listbox.select_set(self.playlist.current_index)
        self.play()

    def exit(self):
        self.player.stop()
        self.master.quit()

    def show_live_visual(self, path):
      
        if self.after_id:
            self.master.after_cancel(self.after_id)
        y, sr = librosa.load(path)
        self.chunk_size = 1024
        self.ptr = 0
        self.y = y
        self.sr = sr
    
        self.fig, self.ax = plt.subplots(figsize=(6, 2))
        self.line = self.ax.bar(range(50), np.zeros(50))
        self.ax.set_ylim(0, 1)
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        if hasattr(self, 'canvas'):
            self.canvas.get_tk_widget().destroy()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas.get_tk_widget().pack(pady=10)
        self.update_visual()

    def update_visual(self):
        if self.ptr + self.chunk_size >= len(self.y):
            return
        chunk = self.y[self.ptr:self.ptr + self.chunk_size]
        self.ptr += self.chunk_size
        fft_vals = np.abs(np.fft.rfft(chunk))[:50]
        max_val = np.max(fft_vals)
        if max_val > 0:
            fft_vals = fft_vals / max_val
        for bar, h in zip(self.line, fft_vals):
            bar.set_height(h)
        self.canvas.draw()
        self.after_id = self.master.after(50, self.update_visual)


if __name__ == "__main__":
    root = tk.Tk()
    gui = MusicGUI(root)
    root.mainloop()
