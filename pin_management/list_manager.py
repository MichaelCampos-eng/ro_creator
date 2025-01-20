from pin_management.table import ConnectionTable
import os
import sys

class DitmcoList():

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.args = []
        self.arg_names = []
        self.table_col_names = []
        self.table: ConnectionTable = None
        self.clear = lambda: os.system('cls')

    def begin_cli(self):
        self.clear()
        while True:
            arg = input(f"Enter {self.fetch_curr_arg_name()}: ")
            try: 
                if self.__is_quit__(arg):
                    self.clear()
                    self.table.save_as()
                    sys.exit()
                self.step(arg)
                self.clear()
                self.table.display()
            except ValueError as e:
                print(str(e))

    def step(self, arg):
        if self.__is_remove__(arg):
            self.table.remove_entry(arg)
            return
        if not self.__valid__(arg):
            raise ValueError("In__valid__ argument, try again!")
        self.args.append(arg)
        if len(self.args) == len(self.arg_names):
            self.__parse_save__()
            self.args = []
            return 

    def fetch_curr_arg_name(self):
        return self.arg_names[len(self.args)]

    def __parse_save__(self):
        self.table.update(self.args)

    def __valid__(self, arg):
        return len(arg) == 1
    
    def __is_remove__(self, command: str):
        return command.split(" ")[0] == "remove"
    
    def __is_quit__(self, command: str):
        return command == "Q"

class WireList(DitmcoList):

    def __init__(self, file_path: str):
        super().__init__(file_path)
        self.arg_names = ["'FROM' (space) 'PIN LEFT'", "'TO'  (space) 'PIN RIGHT'"]
        self.table_col_names = ["FROM", "PIN LEFT", "TO", "PIN RIGHT"]
        self.table = ConnectionTable(self.table_col_names, file_path, "Wire List") 

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
        for arg in self.args:
            parsed_values += arg.split(" ")
        self.table.update(parsed_values)
        

class IsolatedList(DitmcoList):

    def __init__(self, file_path: str):
        super().__init__(file_path)
        self.arg_names = ["'REF DES' (space) 'PIN'"]
        self.table_col_names = ["'REF DES'", "'PIN'"]
        self.table = ConnectionTable(self.table_col_names, file_path, "'Unused Pin List'")

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
        self.table.update(self.args[0].split(" "))

class GroundList(DitmcoList):

    def __init__(self, file_path: str):
        super().__init__(file_path)
        self.arg_names = ["'Connector", "'Ground'"] 
        self.table_col_names = ["'Connector", "'Ground'"]
        self.table = ConnectionTable(self.table_col_names, file_path, "'Ground Connection List'")
    