import csv
import os
import pandas as pd

class StatisticsManager():
    def __init__(self):
        self.__fileName = 'Statitistics/Statisticstable.csv'
        self.__headers = ['ID', 'Algorithm', 'Length Of Path', 'Edges Explored', 'Time Taken', 'Network']
        self.__current_id = self.GetCurrentID()
    
    def AddEntry(self, data):
        os.makedirs(os.path.dirname(self.__fileName), exist_ok=True)

        # Check if the file already exists and has content
        fileExists = os.path.isfile(self.__fileName)
        with open(self.__fileName, mode='a+', newline='') as file:
            writer = csv.writer(file)
            file.seek(0)
            if not fileExists:
                writer.writerow(self.__headers)
            
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

    def GetCurrentID(self):
        if os.path.isfile(self.__fileName):  # Check if the file exists
            with open(self.__fileName, mode='r') as file:
                reader = csv.reader(file)
                rows = list(reader)
                if len(rows) > 1:  # Check if there are data rows
                    # Retrieve the last ID and increment it
                    return int(rows[-1][0]) + 1
        return 1  # Start from ID 1 if file does not exist or is empty
    
    def DeleteEntryByID(self):
        ...

    def GenerateTimeStamp(self):
        ...


if __name__ == '__main__':
    SM = StatisticsManager()
    SM.AddEntry([ 'Dijkstras', 100,20, 2.34, 'London'])
   