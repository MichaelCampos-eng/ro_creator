import pandas as pd
from ..config_classes.config import Config
from ..converter.list_test import *
from ..conn_management.table import DataEntryManager

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

    def set_test(cfg: Config, list: DataEntryManager):
        pass
        
class WireListRo(DitmcoRo):

    def __init__(self, cfg: Config, list: DataEntryManager):
        self.__test__ = WireListTest(list, cfg)
    
    def set_test(self, cfg: Config, list: DataEntryManager):
        self.__test__ = WireListTest(list, cfg)

class UnusedListRo(DitmcoRo):

    def __init__(self, cfg: Config, list: DataEntryManager):
        self.__test__ = UnusedListTest(list, cfg)
    
    def set_test(self, cfg: Config, list: DataEntryManager):
        self.__test__ = UnusedListTest(list, cfg)

class GroundListRo(DitmcoRo):

    def __init__(self, cfg: Config, list: DataEntryManager):
        self.__test__ = GroundListTest(list, cfg)
    
    def set_test(self, cfg: Config, list: DataEntryManager):
        self.__test__ = GroundListTest(list, cfg)

class AggregateRo(DitmcoRo):
    
    def __init__(self, wire_test: WireListTest,
                    isolated_test: UnusedListTest,
                    grd_test: GroundListTest 
                 ):
        self.__error__ = "Empty lists."
        self.__wire_test__ = wire_test
        self.__isolated_test__ = isolated_test
        self.__grd_test__ = grd_test

    def export(self, file_path):
        ro_str = self.__wire_test__.execute() if self.__wire_test__ else ""
        ro_str += self.__isolated_test__.execute() if self.__isolated_test__ else ""
        ro_str += self.__grd_test__.execute() if self.__grd_test__ else ""
        if ro_str != "":
            self.__export_file__(ro_str, file_path)
        else:
            raise ValueError(self.__error_str__)
        
    def set_wire_test(self, test: WireListTest):
        self.__wire_test__ = test
    
    def set_iso_test(self, test: UnusedListTest):
        self.__isolated_test__ = test
    
    def set_grd_test(self, test: GroundListTest):
        self.__grd_test__ = test