import csv
import os
import pandas as pd
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

class StatisticsTableManager():
    def __init__(self):
        self.__fileName = 'Statistics/StatisticsTable.csv'
        self.__headers = ['ID', 'Algorithm', 'Length Of Path', 'Edges Explored', 'Time Taken', 'Network']
        self.__current_id = self.GetCurrentID()
    
    def AddEntry(self, data):
        
        #exist_ok = True stops the directory from being created if already exists
        os.makedirs(os.path.dirname(self.__fileName), exist_ok=True)

        # Check if the file already exists and has content
        #fileExists = os.path.isfile(self.__fileName)
        with open(self.__fileName, mode='a+', newline='') as file:
            writer = csv.writer(file)
            file.seek(0) #Start reading from the top most line
            if not self.HasStatisticsTableFile():
                writer.writerow(self.__headers) #If file did not exist add header
            
            entry = [self.__current_id] + data
            writer.writerow(entry)

            # Increment the ID counter
            self.__current_id += 1


    def DropAllEntries(self):
        table: pd.DataFrame = pd.read_csv(self.__fileName)

# Drop all rows
        table = table.drop(table.index)

        # Save back to CSV
        table.to_csv(self.__fileName, index=False)

        print("CSV file cleared, but headers are retained.")



    def HasStatisticsTableFile(self):
        return os.path.isfile(self.__fileName)
    
    def CreateFilePath(self):
        #exist_ok = True stops the directory from being created if already exists
        os.makedirs(os.path.dirname(self.__fileName), exist_ok=True)
        if not os.path.exists(self.__fileName):
            with open(self.__fileName, 'w') as file:
                writer = csv.writer(file)
                writer.writerow(self.__headers)  

    def GetCurrentID(self):
        if os.path.isfile(self.__fileName):  # Check if the file exists
            with open(self.__fileName, mode='r') as file:
                reader = csv.reader(file)
                rows = list(reader)
                if len(rows) > 1:  # Check if there are data rows
                    # Retrieve the last ID and increment it
                    return int(rows[-1][0]) + 1
        return 1  # Start from ID 1 
    
    def DeleteEntryByID(self, id):
        if not self.HasStatisticsTableFile():
            messagebox.showerror('Error', 'Table has not been created.')
            return 
        if not self.__CheckIDExists(id):
            messagebox.showerror('Error', 'ID does not exist')
            return
        updatedTableData = []
        with open(self.__fileName, mode='r', newline='') as file:
            reader = csv.reader(file)
            headers = next(reader)  # Read the headers
            updatedTableData.append(headers)
            for row in reader:
                    if row and row[0] != str(id):  # Only add the rows we are not deleting
                        updatedTableData.append(row)

        # Write the new data removing missing gaps
        with open(self.__fileName, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(updatedTableData)  


    
    def __CheckIDExists(self, targetID):
        with open(self.__fileName, mode='r') as file:
                reader = csv.reader(file)
                rows = list(reader)
                if self.BinarySearchForID(rows[1:], targetID):
                    return True
                return False

    def BinarySearchForID(self, rows, targetId):
        low = 0
        high = len(rows)-1 
        mid = 0
        while low <= high:
            mid = (high + low) //2
            if int(rows[mid][0]) > targetId:
                high = mid-1
            
            elif int(rows[mid][0]) < targetId:
                low = mid +1
            
            else: 
                print(f'found id {rows[mid][0]}')
                return rows[mid][0]
                
        return None
    
class StatisticsWindow():
    def __init__(self):
        self.__statisticsManager = StatisticsTableManager()
        self.__window = tk.Tk()
        self.__window.title("Statistics Manager")
        self.__window.rowconfigure(0, weight=1)
        self.__window.columnconfigure(0, weight=1)
       
        if not self.__statisticsManager.HasStatisticsTableFile():
            self.__statisticsManager.CreateFilePath()

        self.__dataFrame: pd.DataFrame = pd.read_csv('Statistics/StatisticsTable.csv')
        
        self.tree = ttk.Treeview(self.__window, columns=list(self.__dataFrame.columns), show="headings")
        self.CreateTable()
        
 

        
    def DisplayWindow(self):
        heading = tk.Label(self.__window, text="Statistics Manager", font=("Arial", 16, "bold"))
        heading.grid(row=0, column=0, columnspan=2, pady=10)
        

        deleteAllEntriesBTN = tk.Button(self.__window, text='Delete All Entries', command=self.ClearTable, background='red', foreground='white')
        deleteAllEntriesBTN.grid(row=2, column=0)

        deleteRecordBTN = tk.Button(self.__window, text='Delete  Entry', command=self.__statisticsManager.DropAllEntries, background='red', foreground='white')
        deleteRecordBTN.grid(row=2, column=1)
        
        self.__window.mainloop()

    def ClearTable(self):
        self.__statisticsManager.DropAllEntries()
        self.RefreshTable()


    def CreateTable(self):
        

        # Define column headings
        for col in self.__dataFrame.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)  

        # Insert rows into table
        for _, row in self.__dataFrame.iterrows():
            self.tree.insert("", tk.END, values=list(row))

        self.tree.grid(row=1, column=0, sticky="nsew")

    def RefreshTable(self):
        self.__dataFrame = pd.read_csv("Statitistics/Statisticstable.csv") #Read new updated csv file
        for item in self.tree.get_children(): #delete every old row
            self.tree.delete(item)

        for _, row in self.__dataFrame.iterrows():
            self.tree.insert("", tk.END, values=list(row)) #Insert the new rows



if __name__ == '__main__':
    SM = StatisticsTableManager()
    sw = StatisticsWindow()
    sw.DisplayWindow()
    # for i in range(100):
    #     SM.AddEntry([ 'Dijkstras', 100,20, 2.34, 'London'])
    #SM.DeleteEntryByID(99)
    #SM.CheckIDExists(4)
   