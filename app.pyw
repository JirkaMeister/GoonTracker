import customtkinter
import requests
import threading
from datetime import datetime
from pytz import timezone
from math import ceil
import screeninfo

class App:
    def __init__(self):
        self.root = customtkinter.CTk()
        self.map = "Loading..."
        self.time = "Loading..."
        self.border = False
        self.run()

    def getAPI(self):
        def thread_function():
            response = requests.get('https://tarkovpal.com/api')

            json = response.json()
            self.map = json['Current Map']

            time = datetime.strptime(str(json['Time']), "['%B %d, %Y, %I:%M %p']")

            eastern = timezone('US/Eastern')
            time = eastern.localize(time)
            currentTime = datetime.now(eastern)
            diff = currentTime - time
            self.time = ceil(diff.total_seconds() / 60)
            
        threading.Thread(target = thread_function).start()

    def updateLabels(self):
        try:
            self.labelMapValue.configure(text = self.map)
            self.labelTimeValue.configure(text = f"{self.time} minutes ago")
        finally:
            if self.root:
                self.root.after(1000, self.getAPI)
                self.root.after(1000, self.updateLabels)

    def closeApp(self):
        self.root.destroy()

    def toggleBorder(self):
        self.border = not self.border
        self.root.overrideredirect(not self.border)

    def run(self):
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("dark-blue")

        monitors = screeninfo.get_monitors()
        window_width = 250
        if len(monitors) > 1:
            monitor = monitors[1]
            x = monitor.x + (monitor.width - window_width)

        else:
            screen_width = self.root.winfo_screenwidth()
            x = screen_width - window_width 

        self.root.geometry(f"{window_width}x180+{x}+0")
        self.root.title("Goon tracker")
        self.root.attributes('-topmost', 1)
        self.root.overrideredirect(not self.border)

        self.closeButton = customtkinter.CTkButton(master = self.root, text = "X", command = self.closeApp, width = 20, height = 20, font = ("Arial", 10, "bold"))
        self.closeButton.place(x = window_width - 30, y = 10)

        self.toggleButton = customtkinter.CTkButton(master = self.root, text = "!", command = self.toggleBorder, width = 20, height = 20, font = ("Arial", 10, "bold"))
        self.toggleButton.place(x = window_width - 55, y = 10)

        self.labelTitle = customtkinter.CTkLabel(master = self.root, text = "Goon tracker", font = ("Arial", 20, "bold"))
        self.labelTitle.pack(padx = 20, pady = (10, 0))

        self.frame = customtkinter.CTkFrame(master = self.root)
        self.frame.pack(pady = 20, padx = 20, fill = "both")

        self.labelMap = customtkinter.CTkLabel(master = self.frame, text = "Map:", font = ("Arial", 12, "bold"))
        self.labelMap.grid(row=0, column=0, sticky="e", padx=20, pady=10)

        self.labelMapValue = customtkinter.CTkLabel(master = self.frame, text = self.map)
        self.labelMapValue.grid(row=0, column=1, sticky="w", padx=20, pady=10)

        self.labelTime = customtkinter.CTkLabel(master = self.frame, text = "Time:", font = ("Arial", 12, "bold"))
        self.labelTime.grid(row=1, column=0, sticky="e", padx=20, pady=10)

        self.labelTimeValue = customtkinter.CTkLabel(master = self.frame, text = self.time)
        self.labelTimeValue.grid(row=1, column=1, sticky="w", padx=20, pady=10)

        self.root.after(0, self.getAPI)
        self.root.after(1000, self.updateLabels)
        self.root.mainloop()

App()