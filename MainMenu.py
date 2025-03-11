import tkinter as tk
from tkinter import messagebox
import sys
from DijkstrasDemonstrationWindow import DijkstrasDemonstrationWindow
from Statistics import StatisticsWindow

class MainMenuWindow():
    def __init__(self):
        self.APPLICATION_BUTTON_HEIGHT = 5
        self.APPLICATION_BUTTON_WIDTH = 25

        self.QUIT_BUTTON_HEIGHT = 3
        self.QUIT_BUTTON_WIDTH = 20

        self.root = tk.Tk()
        self.root.title('Main Menu')
        self.root.geometry("1000x400")
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)

        self.mainMenuTitle = tk.Label(self.root, text='Main Menu', font=("Arial", 16, "bold", "underline"))
        self.mainMenuTitle.grid(row=0, column=0, columnspan=2, pady=10)

        

        self.OpenDijkstrasDemonstrationButton = tk.Button(self.root,
                                                          text="Dijkstra's Demonstration",
                                                          height=self.APPLICATION_BUTTON_HEIGHT,
                                                          width=self.APPLICATION_BUTTON_WIDTH,
                                                          font=("Arial", 12, "bold"),
                                                          command=self.OpenDijkstrasDemonstration)
        
        self.OpenDijkstrasDemonstrationButton.grid(row=1, column=1, pady=15, padx=5)
        

        self.OpenMapDemonstrationButton = tk.Button(self.root,
                                                    text='Map Demonstration', 
                                                    height=self.APPLICATION_BUTTON_HEIGHT, 
                                                    width=self.APPLICATION_BUTTON_WIDTH,
                                                    font=("Arial", 12, "bold"),
                                                    command=self.OpenMapDemonstration)
        
        self.OpenMapDemonstrationButton.grid(row=1, column=0, pady=15, padx=5)

        self.OpenStatatisticsWindowButton = tk.Button(self.root,
                                                          text='View Statistics Table',
                                                          height=2,
                                                          width=20,
                                                          font=("Arial", 10),
                                                          command=self.OpenStatisticsWindow)
        
        self.OpenStatatisticsWindowButton.grid(row=2, column=0, columnspan=2,pady=15)


        self.QuitButton = tk.Button(self.root, 
                                    text='Quit',
                                    height=self.QUIT_BUTTON_HEIGHT,
                                    width=self.QUIT_BUTTON_WIDTH,
                                    justify='center',
                                    font=("Arial", 12, "bold"),
                                    command=self.QuitApplication)
        
        self.QuitButton.grid(row=3,column=0, columnspan=2, pady=25)

        #When window is closed via the window manager it is handled the correct way.
        self.root.protocol("WM_DELETE_WINDOW", self.QuitApplication)

    @staticmethod
    def CheckOSMNXInstalled() -> bool:
        isInstalled = False
        try:
            __import__('osmnx')
            isInstalled = True
            return isInstalled
        except ImportError:
            return isInstalled
            



    def QuitApplication(self):
        sys.exit()
    
    def OpenMapDemonstration(self):
        if not MainMenuWindow.CheckOSMNXInstalled(): # Dont open Map demonstration if OSMNX package is not installed.
            messagebox.showerror('Error', 'To use this part of the program ensure you have installed the OSMNX library')
            return
        from Forms import NetworkSettingsInputForm
        self.MinimsieMainMenu()
        networkSettingsForm = NetworkSettingsInputForm(self.root)

    def MinimsieMainMenu(self):
        self.root.iconify()
        
    def OpenStatisticsWindow(self):
        statisticsWindow = StatisticsWindow()
        statisticsWindow.DisplayWindow()
        

    
    def OpenDijkstrasDemonstration(self):
        dijkstrasDemonstrationWindow = DijkstrasDemonstrationWindow()
        dijkstrasDemonstrationWindow.DisplayWindow()
    
    def Run(self): # Begin Tkinter mainloop
        self.root.mainloop()

if __name__ == '__main__':
    mainMenu = MainMenuWindow()
    mainMenu.Run()