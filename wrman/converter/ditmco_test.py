import pandas as pd
from ..config_classes.config import Config
from ..converter.list_test import *

class DitmcoRo:

    """
    A class used to represent an Ro tests for specific list or multiple

    ...

    Attributes
    ----------
    test : BaseListTest
        contains all the tests needed to execute
    __error_str__ : str
        string representation of error

    Methods
    -------
    export_test()
        produces test scripts str and saves it locally using __cfg__
    
    __export_file__(txt: str)
        helper function that export_test uses to save test locally
    """

    def __init__(self):
        self.__error_str__: str
        self.__test__ : BaseListTest
    
    def export(self, file_path):
        try:
            ro_str = self.__test__.execute()
            self.__export_file__(ro_str, file_path)
        except ValueError as e:
            raise ValueError(e)
    
    def __export_file__(self, txt, file_path):
        with open(file_path, 'w') as file:
            file.write(txt)
    
    def get_test(self):
        return self.__test__
        
class WireListRo(DitmcoRo):

    def __init__(self, cfg: Config, wire_list: pd.DataFrame):
        self.__test__ = WireListTest(wire_list, cfg)

class UnusedListRo(DitmcoRo):

    def __init__(self, cfg: Config, isolated_list: pd.DataFrame):
        self.__test__ = UnusedListTest(isolated_list, cfg)

class GroundListRo(DitmcoRo):

    def __init__(self, cfg: Config, ground_list: pd.DataFrame):
        self.__test__ = GroundListTest(ground_list, cfg)

class AggregateRo(DitmcoRo):
    
    def __init__(self, wire_test: WireListTest,
                    isolated_test: UnusedListTest,
                    grd_test: GroundListTest 
                 ):
        self.error = "Empty lists."
        self.wire_test = wire_test
        self.isolated_test = isolated_test
        self.grd_test = grd_test

    def export(self, file_path):
        ro_str = self.wire_test.execute() if self.wire_test else ""
        ro_str += self.isolated_test.execute() if self.isolated_test else ""
        ro_str += self.grd_test.execute() if self.grd_test else ""
        if ro_str != "":
            self.__export_file__(ro_str, file_path)
        else:
            raise ValueError(self.__error_str__)