import pandas as pd
from ..config_classes.config import Config
from ..converter.list_test import *

class DitmcoRo:

    """
    A class used to represent an Ro tests for specific list or multiple

    ...

    Attributes
    ----------
    cfg : COnfig
        metadata describing parameters and types of test to create 
    test : BaseListTest
        contains all the tests needed to execute
    error_str

    Methods
    -------
    export_test()
        produces test scripts str and saves it locally using __cfg__
    
    __export_file__(txt: str)
        helper function that export_test uses to save test locally
    """

    def __init__(self, cfg: Config, ditmco_list: pd.DataFrame = None):
        self.__cfg__ = cfg
        self.__test__ = BaseListTest(ditmco_list, cfg)
        self.__error_str__ = None
    
    def export_test(self):
        try:
            ro_str = self.__test__.execute()
            self.__export_file__(ro_str)
        except ValueError as e:
            raise ValueError(e)
    
    def __export_file__(self, txt):
        with open(self.__cfg__.results_path, 'w') as file:
            file.write(txt)

class AggregateRo(DitmcoRo):
    
    def __init__(self, cfg, wire_df = None, isolated_df = None, ground_df = None):
        super().__init__(cfg)
        self.error = "Empty lists."
        self.wire_list = WireListTest(wire_df, cfg)
        self.isolated_ro = UnusedListTest(isolated_df, cfg)
        self.ground_ro = GroundListTest(ground_df, cfg)

    def export_test(self):
        ro_str = self.wire_list.execute() if self.wire_list else ""
        ro_str += self.isolated_ro.execute() if self.isolated_ro else ""
        ro_str += self.ground_ro.execute() if self.ground_ro else ""
        if ro_str != "":
            self.__export_file__(ro_str)
        else:
            raise ValueError(self.__error_str__)
        
class WireListRo(DitmcoRo):

    def __init__(self, cfg: Config, wire_list: pd.DataFrame):
        self.__cfg__ = cfg
        self.__test__ = WireListTest(wire_list, cfg)
        self.__error_str__ = "Wire list is empty."

class UnusedListRo(DitmcoRo):

    def __init__(self, cfg: Config, isolated_list: pd.DataFrame):
        self.__cfg__ = cfg
        self.__test__ = UnusedListTest(isolated_list, cfg)
        self.__error_str__ = "Wire list is empty."

class GroundListRo(DitmcoRo):

    def __init__(self, cfg: Config, ground_list: pd.DataFrame):
        self.__cfg__ = cfg
        self.__test__ = GroundListTest(ground_list, cfg)
        self.__error_str__ = "Ground list is empty."
