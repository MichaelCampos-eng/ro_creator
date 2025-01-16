from pin_management.table import ConnectionTable
import os
import sys

class DitmcoList():

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.arg_names = []
        self.table_col_names = []
        self.table: ConnectionTable = None
        self.clear = lambda: os.system('cls') 

    def begin_manual(self):
        self.clear()
        while True:
            values = []
            for column in self.arg_names:
                arg = input(f"Enter {column}: ")
                if arg == "Q":
                    self.clear()
                    self.table.save_as()
                    sys.exit()
                if self.table.is_remove(arg):
                    self.table.remove_entry(arg)
                    continue
                if not self.valid_args(arg):
                    
                    values = []
                    break
                values.append(arg)
            if len(values) != len(self.arg_names):
                print("Invalid args, try again")
                continue
            self.save_parsed(values)
            self.clear()
            self.table.display()
            values = []
    
    # TODO: Object detection needs to be done first
    def begin_auto(self):
        pass

    def save_parsed(self, values):
        self.table.update(values)

    def valid_args(self, value):
        return len(value) == 1

class WireList(DitmcoList):

    def __init__(self, file_path: str):
        super().__init__(file_path)
        self.arg_names = ["'FROM' (space) 'PIN LEFT'", "'TO'  (space) 'PIN RIGHT'"]
        self.table_col_names = ["FROM", "PIN LEFT", "TO", "PIN RIGHT"]
        self.table = ConnectionTable(self.table_col_names, file_path, "Wire List") 

    def valid_args(self, arg):
        args = arg.split(" ")
        if arg.isspace():
            return False
        if len(args) != 2:
            return False
        if args[0] == '' or args[1] == '':
            return False
        return True
        
    def save_parsed(self, args):
        values = []
        for arg in args:
            values += arg.split(" ")
        self.table.update(values)
        

class IsolatedList(DitmcoList):

    def __init__(self, file_path: str):
        super().__init__(file_path)
        self.arg_names = ["'REF DES'", "'PIN'"]
        self.table_col_names = ["'REF DES'", "'PIN'"]
        self.table = ConnectionTable(self.column_names, file_path, "'Unused Pin List'")

class GroundList(DitmcoList):

    def __init__(self, file_path: str):
        super().__init__(file_path)
        self.arg_names = ["'Connector", "'Ground'"] 
        self.table_col_names = ["'Connector", "'Ground'"]
        self.table = ConnectionTable(self.column_names, file_path, "'Ground Connection List'")
    