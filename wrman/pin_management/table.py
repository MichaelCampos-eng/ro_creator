import pandas as pd
import random as rd

class ConnectionTable:
    
    def __init__(self, column_names, table_name):
        self.table_name = table_name
        self.df = pd.DataFrame(columns=column_names)

    def open(self, csv_path):
        self.df = pd.read_csv(csv_path)

    def save_as(self, file_path):
        table_name = self.table_name.replace(" ", "_").lower()
        serial_num = ''.join([str(rd.randint(0, 9)) for _ in range(5)])
        file_full_name = f"{file_path}/{table_name}_{serial_num}.csv"
        print(f"\nSaving dataframe as {file_full_name}...")
        self.df.to_csv(file_full_name, index=False)
        print("Saved!\n")

    def display(self):
        print("\n======================")
        print(self.table_name)
        print(self.df)
        print("======================\n")

    def remove_entry(self, command: str):
        try: 
            index = int(command.split(" ")[1])
            self.df.drop(index, inplace=True)
            self.df.reset_index(drop=True, inplace=True)
            self.display()
            print(f"Entry at index {index} removed\n")
        except Exception as e:
            print(f"Invalid index: {command[1]}")

    def update(self, values):
        new_entry = pd.DataFrame({self.df.columns[i]: [values[i].replace(" ", "")] for i in range(len(self.df.columns))})
        self.df = pd.concat([self.df, new_entry])
        indices = self.df.apply(lambda row: tuple(sorted(row)), axis=1).drop_duplicates().reset_index(drop=True).index.to_list()
        self.df = self.df.iloc[indices].reset_index().drop(columns=["index"])
    