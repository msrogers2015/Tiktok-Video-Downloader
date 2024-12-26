import json
import requests
import tkinter as tk
from tkinter import messagebox, filedialog


class App:
    def __init__(self, data):
        self.data = data
        self.links = []
        self.counter = 1
        self.load_data()
        self. cycle_videos()
    
    def cycle_videos(self):
        for link in self.links:
            self.save_video(link)

    def load_data(self):
        with open(self.data, 'r', encoding='utf8') as file:
            data = json.load(file)
            video_list = data['Video']['Videos']['VideoList']
            for video in video_list:
                self.links.append(video['Link'])

    def save_video(self, video):
        for video in self.links:
            vid = requests.get(video)
            # Insert code for GUI updates here
            try:
                with open(f'tiktok_{self.counter}.mov', 'wb') as file:
                    file.write(vid.content)
            except Exception as e:
                print(e)
            self.counter += 1

if __name__ == '__main__':
    #root = tk.Tk()
    file = filedialog.askopenfile()
    app = App(file.name)