from ..conn_management.table import ConnectionTable
from ..utils.labels import *
import os
import sys
import pandas as pd
from typing import List

PIN_LEFT = WL.PIN_LEFT.value
PIN_RIGHT = WL.PIN_RIGHT.value
FROM = WL.FROM.value
TO = WL.TO.value
CONNECTOR = CL.CONNECTOR.value
PIN = CL.PIN.value
GROUND = CL.GROUND.value

class DitmcoList():
    """
    A class used to represent Ditmco list
    Two capabilties:
        1) Using command line interface with begin_cli function
        2) Using api with step fuction

    ...

    Attributes
    ----------
    __args__ : List[str]
        list of column entries for table

    __hint_txts__ : List[str]
        list of placeholder texts displayed to inform what arg to input
    
    __table_col_names__ : List[str]
        list of column names for table
    
    __table__ : ConnectionTable
        ConnectionTable to store entries for list

    Methods
    -------
    __clear__()
        clear the command line interface
    
    begin_cli(file_path: str)
        manually input args into cli to create table and saves csv in file_path

    step(arg: str):
        updates __args__ after verifying validity and parsing given input arg, 
        saving entry if num of __args__ is of num of col of __table__
    
    load_list(file_path):
        loads csv file from file_path into __table__ and clears __args__
    
    save_list(file_path):
        save csv file from __table__ into file_path and clears __args__
    
    get_list_name():
        returns name of __table__
    
    get_df():
        returns raw pd.DataFrame from __table__
    
    get_column_names()
        returns column names of __table__
    
    fetch_hint_text()
        returns current arg needed to be inputted
    
    __parse_save__()
        parses __args__ and saves it in __table__ as row entry
    
    __valid__()
        returns true if inputted arg is valid else false
    
    __is_remove__()
        return true if arg is of command remove else false
    
    __is_quit__()
        return true if arg is command quit else false
    
    """

    def __init__(self):
        self.__args__ = []
        self.__hint_txts__ = []
        self.__table_col_names__ = []
        self.__table__: ConnectionTable = None
        self.__clear__ = lambda: os.system('cls')

    def begin_cli(self, folder_path: str):
        self.__clear__()
        while True:
            arg = input(f"Enter {self.fetch_hint_txt()}: ")
            try: 
                if self.__is_quit__(arg):
                    self.__clear__()
                    self.__table__.save_in(folder_path=folder_path)
                    sys.exit()
                self.step(arg)
                self.__clear__()
                self.__table__.display()
            except ValueError as e:
                print(str(e))

    def step(self, arg: str):
        if self.__is_remove__(arg):
            try: 
                self.__table__.remove_entry(arg)
                return
            except Exception as e:
                raise e
        if not self.__valid__(arg):
            raise ValueError("Invalid argument, try again!")
        self.__args__.append(arg)
        if len(self.__args__) == len(self.__hint_txts__):
            self.__parse_save__()
            self.__args__ = []
            return 
    
    def load_list(self, file_path: str):
        self.__table__.open(file_path)
        self.__args__ = []

    def save_list(self, file_path: str):
        self.__table__.save_as(file_path)
        self.__args__ = []
        
    def get_list_name(self) -> str:
        return self.__table__.table_name
    
    def get_df(self) -> pd.DataFrame:
        return self.__table__.df
    
    def get_column_names(self) -> List[str]:
        return self.__table_col_names__

    def fetch_hint_txt(self) -> str:
        return self.__hint_txts__[len(self.__args__)]

    def __parse_save__(self):
        self.__table__.add_entry(self.__args__)

    def __valid__(self, arg) -> bool:
        args = arg.split(" ")
        if arg.isspace():
            return False
        if len(args) != 2:
            return False
        if args[0] == '' or args[1] == '':
            return False
        return True
        
    def __is_remove__(self, command: str) -> bool:
        return command.split(" ")[0] == "remove"
    
    def __is_quit__(self, command: str) -> bool:
        return command == "Q"

class WireList(DitmcoList):

    def __init__(self):
        super().__init__()
        self.__hint_txts__ = ["'FROM' (space) 'PIN LEFT'", "'TO'  (space) 'PIN RIGHT'"]
        self.__table_col_names__ = [FROM, PIN_LEFT, TO, PIN_RIGHT]
        self.__table__ = ConnectionTable(self.__table_col_names__, "Wire List") 
        
    def __parse_save__(self):
        parsed_values = []
        for arg in self.__args__:
            parsed_values += arg.split(" ")
        self.__table__.add_entry(parsed_values)
        

class IsolatedList(DitmcoList):

    def __init__(self):
        super().__init__()
        self.__hint_txts__ = ["'REF DES' (space) 'PIN'"]
        self.__table_col_names__ = [CONNECTOR, PIN]
        self.__table__ = ConnectionTable(self.__table_col_names__, "Unused Pin List")
    
    def __parse_save__(self):
        self.__table__.add_entry(self.__args__[0].split(" "))

class GroundList(DitmcoList):

    def __init__(self):
        super().__init__()
        self.__hint_txts__ = ["'Connector'", "'Ground'"] 
        self.__table_col_names__ = [CONNECTOR, GROUND]
        self.__table__ = ConnectionTable(self.__table_col_names__, "Ground List")
    
    def __valid__(self, arg) -> bool:
        if self.__is_remove__(arg):
            return True
        if arg.isspace() or arg == "":
            return False
        args = arg.split(" ")
        return len(args) == 1
    