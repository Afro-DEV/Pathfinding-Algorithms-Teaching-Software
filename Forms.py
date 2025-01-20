import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from Utilities import CharacterToId, IdToCharacter

class GraphGeneratorForm():
    def __init__(self):
        self.numberOfNodes = 5
        self.pValue = 50

        self.root = tk.Tk()
        self.root.title('Graph Form')
        self.root.geometry("400x370")
        self.root.resizable(False, False)

        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)

        self.titleLabel = tk.Label(self.root, text="Graph Generator Form", font=("Arial", 16, "bold"))
        self.titleLabel.grid(row=0, column=0, columnspan=2, pady=20)

        self.numberOfNodesLabel = tk.Label(self.root, text="Select number of Nodes", font=("Arial", 12))
        self.numberOfNodesLabel.grid(row=1,column=0, padx=10, pady=5, sticky="e")

        self.numberOfNodesVar = tk.StringVar()
        self.numberOfNodesVar.set("5") 
        self.numberOfNodesOptions = [str(i) for i in range (2,7)]

        self.numberOfNodesDropdown = ttk.Combobox(self.root, textvariable=self.numberOfNodesVar, values=self.numberOfNodesOptions, state="readonly", width=5, font=("Arial", 12))
        self.numberOfNodesDropdown.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        #Bind the selection to the handler
        self.numberOfNodesDropdown.bind("<<ComboboxSelected>>", self.OnSelectedNumberOfNodes)

        self.sliderInfoLabel = tk.Label(self.root, text="Drag slider for how connected graph should be", font=("Arial", 12, "italic"))
        self.sliderInfoLabel.grid(row=2, column=0, columnspan=2, pady=5)
        

        self.slider = tk.Scale(self.root, from_=0, to=100, orient="horizontal", command=self.OnSelectedPValue,  font=("Arial", 12))
        self.slider.set(self.pValue)
        self.slider.grid(row=3, column=0, columnspan=2, padx=10, sticky="ew")

        self.sliderLabelLeft = tk.Label(self.root, text="Sparsely Connected", font=("Arial", 12))
        self.sliderLabelLeft.grid(row=4, column=0, padx=10, pady=10, sticky="w")

        self.sliderLabelRight = tk.Label(self.root, text="Highly Connected", font=("Arial", 12))
        self.sliderLabelRight.grid(row=4, column=1)

        self.submitButton = tk.Button(self.root, text="Submit", command=self.Submit, width=10, height=2)
        self.submitButton.grid(row=5, column=0, columnspan=2, pady=30)


        

        
        
    def OnSelectedNumberOfNodes(self, event):
        self.numberOfNodes = self.numberOfNodesVar.get()
    
    def OnSelectedPValue(self, event):
        self.pValue = self.slider.get()
     
    def Run(self):
        self.root.mainloop()

    def Submit(self):
        self.root.quit()
        self.root.destroy() 



class SourceNodeInputForm():
    def __init__(self, numNodes):
        self.root = tk.Tk()
        self.root.title('Form')
        self.root.geometry("200x125")
        #self.root.title("Source Node Input Form")
        self.numNodes = numNodes

        self.label = tk.Label(self.root, text=f"Enter The Source Node from range A -{IdToCharacter(self.numNodes-1)}:", wraplength=150)
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
            messagebox.showerror("Error", "Input must only contain a single alphabetic Character. Please enter a character")
            return
        elif  userInput < 'A'  or userInput > IdToCharacter(self.numNodes):
            messagebox.showerror("Error", f"Input must be in range A -{IdToCharacter(self.numNodes-1)}. Please enter a character")
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

if __name__ == "__main__":
    app =GraphGeneratorForm()
    app.Run()