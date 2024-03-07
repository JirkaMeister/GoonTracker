import customtkinter
import requests
import threading
from datetime import datetime, timedelta
from pytz import timezone
from math import ceil
import screeninfo

# Main class to run the app
class App:
    def __init__(self):
        self.root = customtkinter.CTk()
        self.map = "Loading..."
        self.time = "Loading..."
        self.lastRotation = "Loading..."
        self.border = False
        self.run()

    # Function to get the information from the API
    def getAPI(self):
        def thread_function():
            # Get the information from the API
            response = requests.get('https://tarkovpal.com/api').json()
    
            newMap = response['Current Map']
            
            self.time = datetime.strptime(str(response['Time']), "['%B %d, %Y, %I:%M %p']")

            # If the map has changed, update the map and the last rotation time
            if newMap != self.map:
                self.map = newMap
                self.lastRotation = self.time
            
        # Multithreading to avoid freezing the GUI
        threading.Thread(target = thread_function).start()

    # Function to update the labels with new information
    def updateLabels(self):
        try:
            # Converting timestamps to minute differences
            eastern = timezone('US/Eastern')
            
            time = eastern.localize(self.time)
            lastRotation = eastern.localize(self.lastRotation)

            currentTime = datetime.now(eastern)

            timeDiff = currentTime - time
            timeDiff = ceil(timeDiff.total_seconds() / 60)

            rotationDiff = currentTime - lastRotation
            rotationDiff = ceil(rotationDiff.total_seconds() / 60)

            # Updating the labels
            self.labelMapValue.configure(text = self.map)
            self.labelTimeValue.configure(text = f"{timeDiff} minutes ago")
            self.labelRotationValue.configure(text = f"{rotationDiff} minutes ago")
        finally:
            # If the window is still open, keep updating the informations
            if self.root:
                self.root.after(1000, self.getAPI)
                self.root.after(1000, self.updateLabels)

    # Function to close the app
    def closeApp(self):
        self.root.destroy()

    # Function to toggle the border (overrideredirect)
    def toggleBorder(self):
        self.border = not self.border
        self.root.overrideredirect(not self.border)

    # Function to run the app
    def run(self):
        # Setting the color theme
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("dark-blue")

        # Getting monitor information
        monitors = screeninfo.get_monitors()
        window_width = 250
        window_height = 210
        if len(monitors) > 1:
            monitor = monitors[1]
            x = monitor.x + (monitor.width - window_width)

        else:
            screen_width = self.root.winfo_screenwidth()
            x = screen_width - window_width 

        # Setting the window position and size
        self.root.geometry(f"{window_width}x{window_height}+{x}+0")
        self.root.resizable(False, False)
        self.root.overrideredirect(not self.border)

        # Setting the window properties
        self.root.title("Goon tracker")
        self.root.attributes('-topmost', 1)
        
        # Buttons to close the app and toggle the border
        self.closeButton = customtkinter.CTkButton(master = self.root, text = "X", command = self.closeApp, width = 20, height = 20, font = ("Arial", 10, "bold"))
        self.closeButton.place(x = window_width - 25, y = 5)

        self.toggleButton = customtkinter.CTkButton(master = self.root, text = "!", command = self.toggleBorder, width = 20, height = 20, font = ("Arial", 10, "bold"))
        self.toggleButton.place(x = window_width - 50, y = 5)

        # Labels to show the information
        self.labelTitle = customtkinter.CTkLabel(master = self.root, text = "Goon tracker", font = ("Arial", 20, "bold"))
        self.labelTitle.pack(padx = 20, pady = (10, 0))

        self.frame = customtkinter.CTkFrame(master = self.root, fg_color='#1C1C1C')
        self.frame.pack(pady = (10, 20), padx = 20, fill = "both")

        self.labelMap = customtkinter.CTkLabel(master = self.frame, text = "Map:", font = ("Arial", 12, "bold"))
        self.labelMap.grid(row=0, column=0, sticky="e", padx=20, pady=10)

        self.labelMapValue = customtkinter.CTkLabel(master = self.frame, text = self.map)
        self.labelMapValue.grid(row=0, column=1, sticky="w", padx=(0, 20), pady=10)

        self.labelTime = customtkinter.CTkLabel(master = self.frame, text = "Time:", font = ("Arial", 12, "bold"))
        self.labelTime.grid(row=1, column=0, sticky="e", padx=20, pady=10)

        self.labelTimeValue = customtkinter.CTkLabel(master = self.frame, text = self.time)
        self.labelTimeValue.grid(row=1, column=1, sticky="w", padx=(0, 20), pady=10)

        self.labelRotation = customtkinter.CTkLabel(master = self.frame, text = "Rotation:", font = ("Arial", 12, "bold"))
        self.labelRotation.grid(row=2, column=0, sticky="e", padx=20, pady=10)

        self.labelRotationValue = customtkinter.CTkLabel(master = self.frame, text = self.lastRotation)
        self.labelRotationValue.grid(row=2, column=1, sticky="w", padx=(0, 20), pady=10)

        # Planning the update functions
        self.root.after(0, self.getAPI)
        self.root.after(1000, self.updateLabels)

        # Running the app
        self.root.mainloop()

if __name__ == "__main__":
    App()