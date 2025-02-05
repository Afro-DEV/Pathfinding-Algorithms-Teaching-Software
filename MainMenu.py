import tkinter as tk
from tkinter import messagebox
import sys
from DijkstrasMainWindow import Window
from Forms import NetworkSettingsInputForm
class MainMenu():
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
                                                          text='Dijkstras Demonstration',
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


        self.QuitButton = tk.Button(self.root, 
                                    text='Quit',
                                    height=self.QUIT_BUTTON_HEIGHT,
                                    width=self.QUIT_BUTTON_WIDTH,
                                    justify='center',
                                    font=("Arial", 12, "bold"),
                                    command=self.QuitApplication)
        
        self.QuitButton.grid(row=2, columnspan=2, pady=25)

    def QuitApplication(self):
        sys.exit()
    
    def OpenMapDemonstration(self):
        networkSettingsForm = NetworkSettingsInputForm(self.root)
        
        #messagebox.showerror('Error', 'To use this part of the program ensure you have installed the osmnx Libary')
            
        

    
    def OpenDijkstrasDemonstration(self):
        dijkstrasDemonstrationWindow = Window()
        dijkstrasDemonstrationWindow.DisplayWindow()
    
    def Run(self):
        self.root.mainloop()

if __name__ == '__main__':
    mainMenu = MainMenu()
    mainMenu.Run()