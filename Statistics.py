import csv
import os
import pandas as pd

class StatisticsManager():
    def __init__(self):
        self.__fileName = 'Statitistics/Statisticstable.csv'
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

    
    def PreviewEntries(self):
        ...

    def HasStatisticsTableFile(self):
        return os.path.isfile(self.__fileName)

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


    def GenerateTimeStamp(self):
        ...
    
    def CheckIDExists(self, targetID):
        currentIds = []
        with open(self.__fileName, mode='r') as file:
                reader = csv.reader(file)
                rows = list(reader)
                self.BinarySearchForID(rows[1:], targetID)
        print(currentIds)

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
                
        print('no id ')
        return 'ID not present'
if __name__ == '__main__':
    SM = StatisticsManager()
    # SM.AddEntry([ 'Dijkstras', 100,20, 2.34, 'London'])
    # SM.DeleteEntryByID(99)
    SM.CheckIDExists(99)
   