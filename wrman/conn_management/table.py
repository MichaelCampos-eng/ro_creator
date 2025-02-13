from typing import List
import pandas as pd
import random as rd
import zipfile
import io

class DataEntryManager:

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
        self.__table_name__ = table_name
        self.__df__ = pd.DataFrame(columns=column_names)
        self.__result_str__ = None

    def open_parquet(self, file: zipfile.ZipExtFile):
        opened: pd.DataFrame = pd.read_parquet(io.BytesIO(file.read()))
        if opened.columns.to_list() != self.__df__.columns.to_list():
            raise ValueError("Invalid spreadsheet. Check table type.")
        self.__df__ = opened

    def open(self, csv_path: str):
        opened: pd.DataFrame = pd.read_csv(csv_path)
        if opened.columns.to_list() != self.__df__.columns.to_list():
            raise ValueError("Invalid spreadsheet. Check table type.")
        self.__df__ = opened

    def save_in(self, folder_path: str):
        __table_name__ = self.__table_name__.replace(" ", "_").lower()
        serial_num = ''.join([str(rd.randint(0, 9)) for _ in range(5)])
        file_full_name = f"{folder_path}/{__table_name__}_{serial_num}.csv"
        self.__df__.to_csv(file_full_name, index=False)
        self.__result_str__ = f"Saved dataframe as {file_full_name}!\n"

    def save_as(self, file_path: str):
        self.__df__.to_csv(file_path, index=False)

    def is_df_empty(self) -> bool:
        return self.__df__.empty
    
    def get_df(self) -> pd.DataFrame:
        return self.__df__
    
    def get_table_name(self) -> str:
        return self.__table_name__

    def display(self):
        if self.__result_str__:
            print("\n" + "#" * 40)
            print(self.__result_str__)
            print("#" * 40 + "\n")

    def remove_entry(self, command: str):
        try: 
            index = int(command.split(" ")[1])
            self.__df__.drop(index, inplace=True)
            self.__df__.reset_index(drop=True, inplace=True)
            self.__result_str__ = f"{self.__table_name__}\n{self.__df__} \n" + f"Entry at index {index} removed\n"
        except Exception as e:
            raise ValueError(f"Invalid index: {command.split(' ')[1]}") from e

    def add_entry(self, values: List[str]):
        new_entry = pd.DataFrame({self.__df__.columns[i]: [values[i].replace(" ", "")] for i in range(len(self.__df__.columns))})
        self.__df__ = pd.concat([self.__df__, new_entry])
        indices = self.__df__.apply(lambda row: tuple(sorted(row.astype(str))), axis=1).drop_duplicates().reset_index(drop=True).index.to_list()
        self.__df__ = self.__df__.iloc[indices].reset_index().drop(columns=["index"])
        self.__result_str__ = f"{self.__table_name__}\n{self.__df__}"
    