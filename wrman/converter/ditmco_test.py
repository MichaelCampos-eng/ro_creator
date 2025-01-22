import pandas as pd
from config_classes.config import Config
from converter.list_test import *
from typing import List

class DitmcoTests:

    def __init__(self, 
                 cfg: Config,
                 wirelist: pd.DataFrame = None, 
                 unused_pins: pd.DataFrame = None,
                 grd_pins: pd.DataFrame = None
                 ):
        self.cfg = cfg
        self.wl_test = WireListTest(wirelist, cfg)
        self.up_test = UnusedListTest(unused_pins, cfg)
        self.grd_test =GroundListTest(grd_pins, cfg)
    
    def execute_tests(self):
        return self.wl_test.execute() + self.up_test.execute() + self.grd_test.execute()

    def export_tests(self): 
        with open(self.cfg.results_path, 'w') as file:
            file.write(self.execute_tests())