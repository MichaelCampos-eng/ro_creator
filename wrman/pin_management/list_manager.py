from ..pin_management.table import ConnectionTable
import os
import sys
import pandas as pd

class DitmcoList():

    def __init__(self):
        self.__args__ = []
        self.__arg_names__ = []
        self.__table_col_names__ = []
        self.__table__: ConnectionTable = None
        self.__clear__ = lambda: os.system('cls')
    
    def import_list(self, csv_path):
        self.__table__.open(csv_path)
        self.__args__ = []

    def begin_cli(self, file_path):
        self.__clear__()
        while True:
            arg = input(f"Enter {self.fetch_curr_arg_name()}: ")
            try: 
                if self.__is_quit__(arg):
                    self.__clear__()
                    self.__table__.save_as(file_path=file_path)
                    sys.exit()
                self.step(arg)
                self.__clear__()
                self.__table__.display()
            except ValueError as e:
                print(str(e))

    def step(self, arg):
        if self.__is_remove__(arg):
            self.__table__.remove_entry(arg)
            return
        if not self.__valid__(arg):
            raise ValueError("In__valid__ argument, try again!")
        self.__args__.append(arg)
        if len(self.__args__) == len(self.__arg_names__):
            self.__parse_save__()
            self.__args__ = []
            return 
    
    def export_list(self, file_path):
        self.__table__.save_as(file_path)
        
    def get_list_name(self) -> str:
        return self.__table__.table_name
    
    def get_table_df(self) -> pd.DataFrame:
        return self.__table__.df
    
    def get_column_names(self):
        return self.__table_col_names__

    def fetch_curr_arg_name(self):
        return self.__arg_names__[len(self.__args__)]

    def __parse_save__(self):
        self.__table__.update(self.__args__)

    def __valid__(self, arg):
        return len(arg) == 1
    
    def __is_remove__(self, command: str):
        return command.split(" ")[0] == "remove"
    
    def __is_quit__(self, command: str):
        return command == "Q"

class WireList(DitmcoList):

    def __init__(self):
        super().__init__()
        self.__arg_names__ = ["'FROM' (space) 'PIN LEFT'", "'TO'  (space) 'PIN RIGHT'"]
        self.__table_col_names__ = ["FROM", "PIN LEFT", "TO", "PIN RIGHT"]
        self.__table__ = ConnectionTable(self.__table_col_names__, "Wire List") 

    def __valid__(self, arg):
        args = arg.split(" ")
        if arg.isspace():
            return False
        if len(args) != 2:
            return False
        if args[0] == '' or args[1] == '':
            return False
        return True
        
    def __parse_save__(self):
        parsed_values = []
        for arg in self.__args__:
            parsed_values += arg.split(" ")
        self.__table__.update(parsed_values)
        

class IsolatedList(DitmcoList):

    def __init__(self):
        super().__init__()
        self.__arg_names__ = ["'REF DES' (space) 'PIN'"]
        self.__table_col_names__ = ["'REF DES'", "'PIN'"]
        self.__table__ = ConnectionTable(self.__table_col_names__, "'Unused Pin List'")

    def __valid__(self, arg):
        args = arg.split(" ")
        if arg.isspace():
            return False
        if len(args) != 2:
            return False
        if args[0] == '' or args[1] == '':
            return False
        return True
    
    def __parse_save__(self):
        self.__table__.update(self.__args__[0].split(" "))

class GroundList(DitmcoList):

    def __init__(self):
        super().__init__()
        self.__arg_names__ = ["'Connector", "'Ground'"] 
        self.__table_col_names__ = ["'Connector", "'Ground'"]
        self.__table__ = ConnectionTable(self.__table_col_names__, "'Ground Connection List'")
    