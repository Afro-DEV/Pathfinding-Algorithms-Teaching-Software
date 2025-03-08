import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from Utilities import CharacterToId, IdToCharacter
from abc import  abstractmethod, ABC

class AbstractForm(ABC): # Showing this class has abstract methods
    def __init__(self, parentWindow = None): 
        if parentWindow: # If we want form to run independently or as the window from a parent window.
            self.form = tk.Toplevel(parentWindow)
        else:
            self.form = tk.Tk()
        baseHeight = 300
        baseWidth = 400
        self.adjustedHeight, self.adjustedWidth = NormaliseFormSizeOnScaling(self.form, baseHeight, baseWidth)

    def Run(self):
        if isinstance(self.form, tk.Tk):#"""Only call mainloop() if this is the main window"""
            self.form.mainloop()

    def GetForm(self):
        return self.form

    @abstractmethod
    def Submit(self):
        pass

def NormaliseFormSizeOnScaling(root, baseHeight: int, baseWidth: int) -> tuple[int,int]:
    '''Normalise the size of form based on Screen Scaling'''
    scaling = root.tk.call('tk', 'scaling')
    return int(baseHeight*scaling), int(baseWidth* scaling)

class GraphGeneratorForm(AbstractForm):
    def __init__(self):
        AbstractForm.__init__(self)
        self.numberOfNodes = 5
        self.pValue = 50
        self.isDemoModeSelected = False
        
        self.form.title('Graph Form')


        baseHeight = 300
        baseWidth = 400
        adjustedHeight, adjustedWidth = NormaliseFormSizeOnScaling(self.form, baseHeight, baseWidth)

        self.form.geometry(f"{adjustedWidth}x{adjustedHeight}")
        #self.root.resizable(False, False)

        self.form.columnconfigure(0, weight=1)
        self.form.columnconfigure(1, weight=1)

        self.titleLabel = tk.Label(self.form, text="Graph Generator Form", font=("Arial", 16, "bold"))
        self.titleLabel.grid(row=0, column=0, columnspan=2, pady=20)

        self.numberOfNodesLabel = tk.Label(self.form, text="Select number of Nodes", font=("Arial", 12))
        self.numberOfNodesLabel.grid(row=1,column=0, padx=10, pady=5, sticky="e")

        self.numberOfNodesVar = tk.StringVar()
        #Setting default value to 5
        self.numberOfNodesVar.set("5") 
        self.numberOfNodesOptions = [str(i) for i in range (2,9)]

        self.numberOfNodesDropdown = ttk.Combobox(self.form, textvariable=self.numberOfNodesVar, values=self.numberOfNodesOptions, state="readonly", width=5, font=("Arial", 12))
        self.numberOfNodesDropdown.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        #Bind the selection to the handler
        self.numberOfNodesDropdown.bind("<<ComboboxSelected>>", self.OnSelectedNumberOfNodes)

        self.sliderInfoLabel = tk.Label(self.form, text="Drag slider for how connected graph should be", font=("Arial", 12, "italic"))
        self.sliderInfoLabel.grid(row=2, column=0, columnspan=2, pady=5)
        

        self.slider = tk.Scale(self.form, from_=0, to=100, orient="horizontal", command=self.OnSelectedPValue,  font=("Arial", 12))
        #Setting the default value of pValue which is 50
        self.slider.set(self.pValue)
        self.slider.grid(row=3, column=0, columnspan=2, padx=10, sticky="ew")

        self.sliderLabelLeft = tk.Label(self.form, text="Sparsely Connected", font=("Arial", 12))
        self.sliderLabelLeft.grid(row=4, column=0, padx=10, pady=10, sticky="w")

        self.sliderLabelRight = tk.Label(self.form, text="Highly Connected", font=("Arial", 12))
        self.sliderLabelRight.grid(row=4, column=1)

        style = ttk.Style() #Adding style to the checkbox
        style.configure("TCheckbutton", focuscolor="transparent", highlightthickness=0, padding=5, font=("Arial", 12))  # Removing focus border

        self.demoCheckBox = ttk.Checkbutton(self.form, text='Demo Mode', onvalue=True, offvalue=False, style="TCheckbutton")
        self.demoCheckBox.grid(row=5, column=0, columnspan=2, pady=5)
        # Remove focus highlight (explicitly unfocus the Checkbutton)
        self.demoCheckBox.focus_set()  # Give focus to some other widget if needed, or leave as is
        self.demoCheckBox.tk_focusNext().focus_set()

        self.submitButton = tk.Button(self.form, text="Submit", command=self.Submit, width=10, height=2)
        self.submitButton.grid(row=6, column=0, columnspan=2, pady=30)


        

        
        
    def OnSelectedNumberOfNodes(self, event):
        '''Update number of nodes every time to the dropdown is modified'''
        self.numberOfNodes = int(self.numberOfNodesVar.get())
        print(f"Dropdown selected: {self.numberOfNodes}")
    
    def OnSelectedPValue(self, event):
        '''Update pValue each time the slider is moved'''
        self.pValue = self.slider.get()
     

    def Submit(self):
        try: #Try to get the value in number of nodes as an integer
            selectedValue =  self.numberOfNodesDropdown.get()  
            self.numberOfNodes = int(selectedValue) if selectedValue else 5  # Ensure default is 5
        except ValueError:
            self.numberOfNodes = 5 # Set number of nodes to 5 incase of error.
        self.pValue = self.slider.get()
        #Getting value selected checkbox
        self.isDemoModeSelected = self.demoCheckBox.instate(['selected'])
        self.form.quit()
        self.form.destroy() 
        print(self.GetNumberOfNodes())

    def IsDemoModeSelected(self)-> bool:
        return self.isDemoModeSelected


    def GetNumberOfNodes(self) -> int:
        return self.numberOfNodes
    


class SourceNodeInputForm(AbstractForm):
    def __init__(self, numNodes):
        AbstractForm.__init__(self)
        self.form.title('Form')
        # Normalize the size based on screen scaling
        scaling = self.form.tk.call('tk', 'scaling')
        baseHeight = 125
        baseWidth = 170
        self.adjustedHeight, self.adjustedWidth = NormaliseFormSizeOnScaling(self.form, baseHeight, baseWidth)

        self.form.geometry(f"{self.adjustedWidth}x{self.adjustedHeight}")
        #self.root.title("Source Node Input Form")
        self.numNodes = numNodes

        self.label = tk.Label(self.form, text=f"Enter The Source Node from range A -{IdToCharacter(self.numNodes-1)}:", wraplength=140)
        self.label.pack(pady=10)

        
        self.entry = tk.Entry(self.form, width=5)
        self.entry.pack(pady=5)

        
        self.submitButton = tk.Button(self.form, text="Submit", command=self.Submit)
        self.submitButton.pack(pady=10)

        self.sourceNodeID = None

    def Submit(self):
        userInput = self.entry.get()
        userInput = userInput.upper()
        #Validating user input
        if userInput.strip() == "":
            messagebox.showerror("Error", "Input cannot be empty. Please enter a character")
            return
        elif len(userInput) > 1:
            messagebox.showerror("Error", "Input cannot be more than one character. Please enter a single character")
            return
        elif not userInput.isalpha():
            messagebox.showerror("Error", "Input must only contain a single alphabetic Character. Please enter an alphabetic character")
            return
        elif  userInput < 'A'  or userInput > IdToCharacter(self.numNodes):
            messagebox.showerror("Error", f"Input must be in range A -{IdToCharacter(self.numNodes-1)}. Please enter a character within this range")
            return

        try: #Try to convert Users Selection to ID
            sourceNodeID = CharacterToId(userInput)
            print(sourceNodeID)
            self.sourceNodeID = sourceNodeID
            self.form.quit()
            self.form.destroy() 
            #messagebox.showinfo("Success", f"You entered the SourceNode: {userInput}")
        except:
            messagebox.showerror("Unexpected Error", "Please try again")
           
    

    def GetSourceNodeID(self) -> int:
        return self.sourceNodeID
    

class NetworkSettingsInputForm(AbstractForm):
    def __init__(self, parentWindow):
        super().__init__(parentWindow)  # Pass parent to AbstractForm by calling AbstractForm initialisng method.

        #Initial form Values
        self.algorithmSelected = None
        self.networkSelected = None
        self.useMiles = False

        
        self.form.title('Road Network Settings')
        
        self.form.geometry(f"{self.adjustedWidth}x{self.adjustedHeight}")

        self.form.columnconfigure(0, weight=1)
        self.form.columnconfigure(1, weight=1)
        
        self.titleLabel = tk.Label(self.form, text="Road Network Settings", font=("Arial", 16, "bold"))
        self.titleLabel.grid(row=0, column=0, columnspan=2, pady=20)

        self.numberOfNodesLabel = tk.Label(self.form, text="Select Road Network", font=("Arial", 12))
        self.numberOfNodesLabel.grid(row=1,column=0, padx=10, pady=5, sticky="e")

        self.selectNetworkVar = tk.StringVar()
        self.selectNetworkVar.set("London")
        self.networkOptions = ['London', 'NewYork', 'Paris']

        self.networkDropdown = ttk.Combobox(self.form, textvariable=self.selectNetworkVar, values=self.networkOptions, state="readonly",font=("Arial", 12))
        self.networkDropdown.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        self.networkDropdown.bind("<<ComboboxSelected>>", self.OnSelectedNetwork)

        self.algorithmLabel = tk.Label(self.form, text="Select Algorithm to be used", font=("Arial", 12))
        self.algorithmLabel.grid(row=2, column=0, padx=10, pady=5, sticky="e")

        self.selectAlgorithmVar = tk.StringVar()
        self.selectAlgorithmVar.set('A-Star')
        self.algorithmOptions = ['A-Star', 'Dijkstras']

        self.algorithmDropdown = ttk.Combobox(self.form, textvariable=self.selectAlgorithmVar, values=self.algorithmOptions, state="readonly",font=("Arial", 12))
        self.algorithmDropdown.grid(row=2, column=1, padx=10, pady=10, sticky="w")
        self.algorithmDropdown.bind("<<ComboboxSelected>>", self.OnSelectedAlgorithm)

        self.distanceInMilesCheckBoxLabel = tk.Label(self.form, text='Select for distance in miles. Unchecked leaves distance in Kilometres.', font=("Arial", 12), wraplength=300)
        self.distanceInMilesCheckBoxLabel.grid(row=3,column=0, rowspan=2)

        style = ttk.Style()
        style.configure("TCheckbutton", focuscolor="transparent", highlightthickness=0, padding=5, font=("Arial", 12))  # Removing focus borde
        self.distanceInMilesCheckBox = ttk.Checkbutton(self.form, text='Miles', onvalue=True, offvalue=False, style="TCheckbutton")
        self.distanceInMilesCheckBox.grid(row=3, column=1,  pady=5)
         # Remove focus highlight (explicitly unfocus the Checkbutton)
        self.distanceInMilesCheckBox.focus_set()  # Give focus to some other widget if needed, or leave as is
        self.distanceInMilesCheckBox.tk_focusNext().focus_set()

        self.submitButton = tk.Button(self.form, text="Submit", command=self.Submit, width=10, height=2)
        self.submitButton.grid(row=5, column=0, columnspan=2, pady=30)

    def OnSelectedNetwork(self, event):
        '''Update Network selected variable each time the dropdown  is modified'''
        self.networkSelected = self.selectNetworkVar.get()
        print(f"Network selected is {self.networkSelected}")

    def OnSelectedAlgorithm(self, event):
        self.algorithmSelected = self.selectAlgorithmVar.get()
        print(f"Algorithm selected is {self.algorithmSelected}")

    def GetNetworkSelectedFilePath(self, networkSelected):
        '''Returns parameterised network file based on selected network'''
        return f"Networks/{networkSelected}Network.graphml"


    def Submit(self):
        from MainMenu import MainMenuWindow
        
        #Get current drop down values.
        self.networkSelected = self.selectNetworkVar.get()
        self.algorithmSelected = self.selectAlgorithmVar.get()

        self.useMiles = self.distanceInMilesCheckBox.instate(['selected']) #True if it is selected false if not
        print(f"DEBUG: Submitting with Network={self.networkSelected}, Algorithm={self.algorithmSelected}, UseMiles={self.useMiles}")
        if MainMenuWindow.CheckOSMNXInstalled(): #Only display if necessary packages installed
            from MapDemonstrationWindow import MapDemonstrationWindow
            window = MapDemonstrationWindow(self.networkSelected, algorithm=self.algorithmSelected, useMiles=self.useMiles)
            window.DisplayNetwork()
        else:
            print('OSMNX is not installed')

class StatisticsManagerInputRecordIDForm(AbstractForm):

    def __init__(self):
        AbstractForm.__init__(self)
        self.__deletedID = None
        self.form.title('Form')
        # Normalize the size based on screen scaling
        scaling = self.form.tk.call('tk', 'scaling')
        baseHeight = 125
        baseWidth = 170
        self.adjustedHeight, self.adjustedWidth = NormaliseFormSizeOnScaling(self.form, baseHeight, baseWidth)

        self.form.geometry(f"{self.adjustedWidth}x{self.adjustedHeight}")
        #self.root.title("Source Node Input Form")
        

        self.label = tk.Label(self.form, text=f"Enter record ID to be deleted.", wraplength=140)
        self.label.pack(pady=10)

        
        self.entry = tk.Entry(self.form, width=5)
        self.entry.pack(pady=5)

        
        self.submitButton = tk.Button(self.form, text="Submit", command=self.Submit)
        self.submitButton.pack(pady=10)

        self.sourceNodeID = None

    def Submit(self):
        userInput = self.entry.get()

        if userInput == "":  
            messagebox.showerror("Input Error", "Please enter a number before submitting")
            return  
        
        if not userInput.isdigit():
            messagebox.showerror("Type Error", "Please enter a valid integer")
            return
        
        try: #Try to convert Users Selection to ID
            self.__deletedID = int(userInput)
            self.form.quit()
            self.form.destroy() 
        except:
            messagebox.showerror("Unexpected Error", "Please try again")

    def GetDeletedID(self):
        return self.__deletedID
        
        



if __name__ == "__main__":
    app = StatisticsManagerInputRecordIDForm()
    app.Run()
