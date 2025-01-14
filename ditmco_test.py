import pandas as pd
from config_classes.config import Config
from converter.test import *

class DitmcoTest:

    def __init__(self, cfg: Config):
        self.cfg = cfg
        self.df = pd.read_csv(cfg.csv_path)
    
    def produce_test_ro_file(self):

        """
        continuity_test = ContinuityTest(block_name, params)
        isolation_test = IsolationTest(block_name, params)
        isolation_test = HipotTest(block_name, params)

        continuity_test.run
        
        """ 

        for task in self.cfg.tasks:
            if task.name == "continuity":
                cont_test = ContinuityTest(task.block_name, task.param)
                cont_test.convert_to_test(df=self.df)
        
        return
