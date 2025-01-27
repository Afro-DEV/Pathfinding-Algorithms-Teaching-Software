import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from Utilities import CharacterToId, IdToCharacter

def NormaliseFormSizeOnScaling(root, baseHeight: int, baseWidth: int) -> tuple[int,int]:
    '''Normalise the size of form based on Screen Scaling'''
    scaling = root.tk.call('tk', 'scaling')
    return int(baseHeight*scaling), int(baseWidth* scaling)

class GraphGeneratorForm():
    def __init__(self):
        self.numberOfNodes = 5
        self.pValue = 50
        self.isDemoModeSelected = False
        
        self.root = tk.Tk()
        self.root.title('Graph Form')


        baseHeight = 300
        baseWidth = 400
        adjustedHeight, adjustedWidth = NormaliseFormSizeOnScaling(self.root, baseHeight, baseWidth)

        self.root.geometry(f"{adjustedWidth}x{adjustedHeight}")
        #self.root.resizable(False, False)

        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)

        self.titleLabel = tk.Label(self.root, text="Graph Generator Form", font=("Arial", 16, "bold"))
        self.titleLabel.grid(row=0, column=0, columnspan=2, pady=20)

        self.numberOfNodesLabel = tk.Label(self.root, text="Select number of Nodes", font=("Arial", 12))
        self.numberOfNodesLabel.grid(row=1,column=0, padx=10, pady=5, sticky="e")

        self.numberOfNodesVar = tk.StringVar()
        #Setting default value to 5
        self.numberOfNodesVar.set("5") 
        self.numberOfNodesOptions = [str(i) for i in range (2,9)]

        self.numberOfNodesDropdown = ttk.Combobox(self.root, textvariable=self.numberOfNodesVar, values=self.numberOfNodesOptions, state="readonly", width=5, font=("Arial", 12))
        self.numberOfNodesDropdown.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        #Bind the selection to the handler
        self.numberOfNodesDropdown.bind("<<ComboboxSelected>>", self.OnSelectedNumberOfNodes)

        self.sliderInfoLabel = tk.Label(self.root, text="Drag slider for how connected graph should be", font=("Arial", 12, "italic"))
        self.sliderInfoLabel.grid(row=2, column=0, columnspan=2, pady=5)
        

        self.slider = tk.Scale(self.root, from_=0, to=100, orient="horizontal", command=self.OnSelectedPValue,  font=("Arial", 12))
        #Setting the default value of pValue
        self.slider.set(self.pValue)
        self.slider.grid(row=3, column=0, columnspan=2, padx=10, sticky="ew")

        self.sliderLabelLeft = tk.Label(self.root, text="Sparsely Connected", font=("Arial", 12))
        self.sliderLabelLeft.grid(row=4, column=0, padx=10, pady=10, sticky="w")

        self.sliderLabelRight = tk.Label(self.root, text="Highly Connected", font=("Arial", 12))
        self.sliderLabelRight.grid(row=4, column=1)

        style = ttk.Style()
        style.configure("TCheckbutton", focuscolor="transparent", highlightthickness=0, padding=5, font=("Arial", 12))  # Removing focus borde
        self.demoCheckBox = ttk.Checkbutton(self.root, text='Demo Mode', onvalue=True, offvalue=False, style="TCheckbutton")
        self.demoCheckBox.grid(row=5, column=0, columnspan=2, pady=5)
         # Remove focus highlight (explicitly unfocus the Checkbutton)
        self.demoCheckBox.focus_set()  # Give focus to some other widget if needed, or leave as is
        self.demoCheckBox.tk_focusNext().focus_set()

        self.submitButton = tk.Button(self.root, text="Submit", command=self.Submit, width=10, height=2)
        self.submitButton.grid(row=6, column=0, columnspan=2, pady=30)


        

        
        
    def OnSelectedNumberOfNodes(self, event):
        self.numberOfNodes = int(self.numberOfNodesVar.get())
        print(f"Dropdown selected: {self.numberOfNodes}")
    
    def OnSelectedPValue(self, event):
        self.pValue = self.slider.get()
     
    def Run(self):
        self.root.mainloop()

    def Submit(self):
        try:
            self.numberOfNodes = int(self.numberOfNodesDropdown.get())  # Ensure it's an integer
        except ValueError:
            print('Not entered number of Nodes using 5')
        self.pValue = self.slider.get()
        #Getting value selected checkbox
        self.isDemoModeSelected = self.demoCheckBox.instate(['selected'])
        print(f"Checkbox selected: {self.isDemoModeSelected}")
        self.root.quit()
        self.root.destroy() 
        print(self.GetNumberOfNodes())

    def IsDemoModeSelected(self)-> bool:
        return self.isDemoModeSelected


    def GetNumberOfNodes(self) -> int:
        return self.numberOfNodes
    
    def GetForm(self):
        return self.root


class SourceNodeInputForm():
    def __init__(self, numNodes):
        self.root = tk.Tk()
        self.root.title('Form')
        # Normalize the size based on screen scaling
        scaling = self.root.tk.call('tk', 'scaling')
        baseHeight = 125
        baseWidth = 170
        adjustedHeight, adjustedWidth = NormaliseFormSizeOnScaling(self.root, baseHeight, baseWidth)

        self.root.geometry(f"{adjustedWidth}x{adjustedHeight}")
        #self.root.title("Source Node Input Form")
        self.numNodes = numNodes

        self.label = tk.Label(self.root, text=f"Enter The Source Node from range A -{IdToCharacter(self.numNodes-1)}:", wraplength=140)
        self.label.pack(pady=10)

        
        self.entry = tk.Entry(self.root, width=5)
        self.entry.pack(pady=5)

        
        self.submitButton = tk.Button(self.root, text="Submit", command=self.submit)
        self.submitButton.pack(pady=10)

        self.sourceNodeIndex = None
    def submit(self):
        userInput = self.entry.get()
        userInput = userInput.upper()
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

        try:
            sourceNodeIndex = CharacterToId(userInput)
            print(sourceNodeIndex)
            self.sourceNodeIndex = sourceNodeIndex
            self.root.quit()
            self.root.destroy() 
            #messagebox.showinfo("Success", f"You entered the SourceNode: {userInput}")
        except:
            messagebox.showerror("Unexpected Error", "Please try again")
           
    
    def Run(self):
        self.root.mainloop()

    def GetSourceNodeIndex(self) -> int:
        return self.sourceNodeIndex
    
    def GetForm(self):
        return self.root

if __name__ == "__main__":
    app = GraphGeneratorForm()
    app.Run()
