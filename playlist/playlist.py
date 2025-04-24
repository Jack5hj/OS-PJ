
class Playlist:
    def __init__(self):
        self.songs = []
        self.index = 0

    def add(self, song):
        self.songs.append(song)

    def previous(self):
        self.index = (self.index - 1) % len(self.songs)
        return self.songs[self.index]

    def next(self):
        self.index = (self.index + 1) % len(self.songs)
        return self.songs[self.index]

    def current(self):
        return self.songs[self.index]
