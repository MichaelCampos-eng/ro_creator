from ..converter.ro_tests import *
import pandas as pd
from typing import List

class BaseListTest():

    def __init__(self, df: pd.DataFrame, cfg: Config):
        self.df = df
        self.cfg = cfg
        self.tests: List[BaseRoTest] = []
        self.header = ""
    
    def setup_tests(self) -> None:
        pass

    def execute(self) -> str:
        if not self.df.empty:
            return f"; {self.header}\n" + "".join([test.convert_to_test(self.df) for test in self.tests])
        raise ValueError("Dataframe is empty.")
    
class WireListTest(BaseListTest):

    def __init__(self, df: pd.DataFrame, cfg: Config):
        super().__init__(df, cfg)
        self.setup_tests()
    
    def setup_tests(self) -> None:
        self.header = "Wire List Tests"
        if self.cfg.continuity_cfg.execute:
            self.tests.append(ContinuityTest(self.cfg.continuity_cfg))
        if self.cfg.leakage_cfg.execute:
            self.tests.append(LeakageTest(self.cfg.continuity_cfg))
        if self.cfg.hipot_cfg.execute:
            self.tests.append(HipotTest(self.cfg.continuity_cfg)) 

class UnusedListTest(BaseListTest):

    def __init__(self, df: pd.DataFrame, cfg: Config):
        super().__init__(df, cfg)
        self.setup_tests()
    
    def setup_tests(self) -> None:
        self.header = "Unused Pins Tests"
        if self.cfg.isolation_cfg.execute:
            self.tests.append(IsolationTest(self.cfg.isolation_cfg))

class GroundListTest(BaseListTest):

    def __init__(self, df: pd.DataFrame, cfg: Config):
        super().__init__(df, cfg)
        self.setup_tests()
    
    def setup_tests(self) -> None:
        self.header = "Ground Tests"
        if self.cfg.continuity_cfg.execute:
            self.tests.append(ContinuityTest(self.cfg.continuity_cfg))