import pandas as pd
import random as rd
from typing import List

class ConnectionTable:

    """
    A class used to represent connectors' mappings

    ...

    Attributes
    ----------
    table_name : str
        name of the dataframe table
    df : pd.DataFrame
        dataframe containing all of entries updated
    __result_str__ : str
        comment used to inform of current state    
    
    Methods
    -------
    open(csv_path: str)
       opens df from csv
    
    save_in(folder_path: str)
        converts and saves df locally given folder path
    
    save_as(file_path: str)
        converts and saves df locally given file path 
    
    display()
        prints __result_str__ in cli
    
    remove_entry(command: str)
        removes entry at index given command
    
    add_entry(values: List[str])
        adds entry and removes duplicate given list of col values
    """
    
    def __init__(self, column_names: List[str], table_name: str):
        self.table_name = table_name
        self.df = pd.DataFrame(columns=column_names)
        self.__result_str__ = None

    def open(self, csv_path: str):
        self.df = pd.read_csv(csv_path)

    def save_in(self, folder_path: str):
        table_name = self.table_name.replace(" ", "_").lower()
        serial_num = ''.join([str(rd.randint(0, 9)) for _ in range(5)])
        file_full_name = f"{folder_path}/{table_name}_{serial_num}.csv"
        self.df.to_csv(file_full_name, index=False)
        self.__result_str__ = f"Saved dataframe as {file_full_name}!\n"

    def save_as(self, file_path: str):
        self.df.to_csv(file_path, index=False)

    def display(self):
        if self.__result_str__:
            print("\n" + "#" * 40)
            print(self.__result_str__)
            print("#" * 40 + "\n")

    def remove_entry(self, command: str):
        try: 
            index = int(command.split(" ")[1])
            self.df.drop(index, inplace=True)
            self.df.reset_index(drop=True, inplace=True)
            self.__result_str__ = f"{self.table_name}\n{self.df} \n" + f"Entry at index {index} removed\n"
        except Exception as e:
            raise ValueError(f"Invalid index: {command.split(' ')[1]}") from e

    def add_entry(self, values: List[str]):
        new_entry = pd.DataFrame({self.df.columns[i]: [values[i].replace(" ", "")] for i in range(len(self.df.columns))})
        self.df = pd.concat([self.df, new_entry])
        indices = self.df.apply(lambda row: tuple(sorted(row.astype(str))), axis=1).drop_duplicates().reset_index(drop=True).index.to_list()
        self.df = self.df.iloc[indices].reset_index().drop(columns=["index"])
        self.__result_str__ = f"{self.table_name}\n{self.df}"
    