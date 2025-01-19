import tkinter as tk
from tkinter import messagebox
from Utilities import CharacterToId, IdToCharacter
class SourceNodeInputForm():
    def __init__(self, numNodes):
        self.root = tk.Tk()
        self.root.title('Form')
        self.root.geometry("200x125")
        #self.root.title("Source Node Input Form")
        self.numNodes = numNodes
        # Create a label
        self.label = tk.Label(self.root, text=f"Enter The Source Node from range A -{IdToCharacter(self.numNodes-1)}:", wraplength=150)
        self.label.pack(pady=10)

        # Create an entry widget
        self.entry = tk.Entry(self.root, width=5)
        self.entry.pack(pady=5)

        # Create a submit button
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
        # Run the Tkinter main loop
        self.root.mainloop()

    def GetSourceNodeIndex(self) -> int:
        return self.sourceNodeIndex

if __name__ == "__main__":
    app =SourceNodeInputForm(7)
    app.Run()