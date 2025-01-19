import pandas as pd

class ConnectionTable:
    
    def __init__(self, column_names, file_path, table_name):
        self.file_path = file_path
        self.table_name = table_name
        self.df = pd.DataFrame(columns=column_names)
        self.col_num = len(column_names)

    def save_as(self):
        print(f"\nSaving dataframe as {self.table_name}...")
        self.df.to_csv(f"{self.file_path}/{self.table_name}.csv", index=False)
        print("Saved!\n")

    def display(self):
        print("\n======================")
        print(self.table_name)
        print(self.df)
        print("======================\n")
    
    def is_remove(self, command: str):
        return command.split(" ")[0] == "remove"

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
    