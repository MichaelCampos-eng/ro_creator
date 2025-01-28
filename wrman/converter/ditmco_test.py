import pandas as pd
from ..config_classes.config import Config
from ..converter.list_test import *

class DitmcoRo:

    def __init__(self, cfg: Config, ditmco_list:pd.DataFrame = None):
        self.cfg = cfg
        self.test = BaseListTest(ditmco_list, cfg)
        self.error_str = None
    
    def export_test(self):
        try:
            ro_str = self.test.execute()
            self.__export_file__(ro_str)
        except ValueError as e:
            raise ValueError(e)
    
    def __export_file__(self, txt):
        with open(self.cfg.results_path, 'w') as file:
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
            raise ValueError(self.error_str)
        
class WireListRo(DitmcoRo):

    def __init__(self, cfg: Config, wire_list: pd.DataFrame):
        self.cfg = cfg
        self.test = WireListTest(wire_list, cfg)
        self.error_str = "Wire list is empty."

class UnusedListRo(DitmcoRo):

    def __init__(self, cfg: Config, isolated_list: pd.DataFrame):
        self.cfg = cfg
        self.test = UnusedListTest(isolated_list, cfg)
        self.error_str = "Wire list is empty."

class GroundListRo(DitmcoRo):

    def __init__(self, cfg: Config, ground_list: pd.DataFrame):
        self.cfg = cfg
        self.test = GroundListTest(ground_list, cfg)
        self.error_str = "Ground list is empty."
