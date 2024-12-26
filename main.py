import json
import requests
import tkinter as tk
import threading
from os import path
from tkinter import messagebox, filedialog
import webbrowser


class App:
    def __init__(self):
        self.links = []
        self.counter = 1
        self.format = ''
        self.flag = ''
        self.gui()

    def gui(self):
        self.root = tk.Tk()
        self.root.geometry('500x225')
        self.root.minsize(500,225)
        self.root.title("Tiktok Video Downloader")
        self.root.protocol('WM_DELETE_WINDOW', self.close_window)
        data_file = tk.Label(self.root, text='Load File', font=(None, 14))
        save_location = tk.Label(self.root, text='Save Folder', font=(None, 14))
        save_type = tk.Label(self.root, text='Save Type', font=(None, 14))
        self.data_entry = tk.Entry(self.root, font=(None, 14))
        self.data_btn = tk.Button(self.root, text='...', command=self.select_file, font=(None, 14))
        self.save_entry = tk.Entry(self.root, font=(None, 14))
        self.save_btn = tk.Button(self.root, text='...', command=self.save_location, font=(None, 14))
        file_types = ['MP4-May Take Longer', 'MOV-Standard Format']
        self.ftype = tk.StringVar()
        self.ftype.set('MOV-Faster')
        self.file_type = tk.OptionMenu(self.root, self.ftype, *file_types)
        self.file_type.config(font=(None, 14))
        self.download = tk.Button(self.root, text='Download TikToks', font=(None, 14), command=self.load_data)
        
        data_file.grid(column=0, row=0)
        self.data_entry.grid(column=1, row=0, sticky='nesw')
        self.data_btn.grid(column=2, row=0)
        save_location.grid(column=0, row=1)

        self.save_entry.grid(column=1, row=1, sticky='nesw')
        self.root.columnconfigure(1, weight=1)
        self.save_btn.grid(column=2, row=1)

        save_type.grid(column=0, row=2)
        self.file_type.grid(column=1, row=2, sticky='nesw')

        self.download.grid(column=1, row=3, sticky='nesw')

        self.status = tk.Label(self.root, text='', font=(None, 14))
        self.status.grid(column=1, row=4, sticky='nesw')

        self.create_menu()

        self.root.mainloop()
    
    def cycle_videos(self):
        for link in self.links:
            self.save_video(link)
    
    def save_location(self):
        folder = filedialog.askdirectory()
        if folder is not None:
            self.save_entry.delete(0, 'end')
            self.save_entry.insert(0, folder)

    def select_file(self):
        file = filedialog.askopenfile()
        if file is not None:
            self.data_entry.delete(0, 'end')
            self.data_entry.insert(0, str(file.name))

    def load_data(self):
        if self.data_entry.get() == '':
            messagebox.showerror('No File Selected', 'Please select your tiktok data file.')
        if self.save_entry.get() == '':
            messagebox.showerror('No Folder Selected', 'Please select an output folder')
        if self.save_entry.get() != '' and self.data_entry.get() != '':
            self.flag = True
            with open(self.data_entry.get(), 'r', encoding='utf8') as file:
                data = json.load(file)
                video_list = data['Video']['Videos']['VideoList']
                for video in video_list:
                    self.links.append(video['Link'])
            self.end = self.ftype.get().split('-')[0].lower()
            self.status.config(text=f'Downloading Video {self.counter} out of {len(self.links)}')
            t1 = threading.Thread(target=self.save_video)
            t1.start()

    def save_video(self):
        self.download.config(command=self.cancel_download, text='Cancel Download')
        for i in range(len(self.links)):
            if self.flag:
                output = path.join(self.save_entry.get(), f'tiktok_{self.counter}.{self.end}')
                vid = requests.get(self.links[i])
                self.status.config(text=f'Downloading Video {self.counter+1} out of {len(self.links)}')
                try:
                    with open(output, 'wb') as file:
                        file.write(vid.content)
                except Exception as e:
                    print(e)
                self.counter += 1
        self.download.config(command=self.load_data, text='Download Tiktoks', state='active')
        self.status.config(text='')
        self.cancel_label.config(text='')
        self.flag = ''
        self.counter = 1
        self.links = []
    
    def cancel_download(self):
        self.cancel_label = tk.Label(self.root, text='Attmpeting to cancel')
        self.download.config(state='disabled')
        self.cancel_label.grid(row=5, column=1)
        self.flag = False

    def create_menu(self):
        menubar = tk.Menu(self.root)

        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='Help', menu = help_menu)
        help_menu.add_command(label='Help', command=lambda: webbrowser.open_new('https://github.com/msrogers2015/Tiktok-Video-Downloader/blob/main/README.md'))
        self.root.config(menu=menubar)

    def close_window(self):
        if self.flag is True:
            messagebox.showwarning('Download in progress', 'Cannot close application, download in progress. Attempting to cancel download.')
            self.cancel_download()
        elif self.flag is False:
            messagebox.showinfo('Attempting to Cancel', 'A download is finishing up. Please try again after the file is done')
        if self.flag == '':
            self.root.destroy()


if __name__ == '__main__':
    app = App()