from ..converter.ro_tests import *
import pandas as pd
from typing import List
from ..utils.labels import *

PIN_LEFT = WL.PIN_LEFT.value
PIN_RIGHT = WL.PIN_RIGHT.value
FROM = WL.FROM.value
TO = WL.TO.value

class BaseListTest():

    """
    A class used to represent test for any type of list

    ...

    Attributes
    ----------
    df : pd.DataFrame
        raw dataframe used as data for test conversions
    cfg : Config
        contains metadata pertaining to what tests to execute and other parameters
    tests : List[BaseRoTest]
        list of tests to be executed such as ContinuityTest, LeakageTest, etc.
    header : str
        name for the list that is going to be tested
    Methods
    -------
    setup_tests()
        creates instances of RO tests and appends it to tests according to cfg
    
    execute()
        if df is not empty, return str of all ro tests based on tests attribute
    """

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
        self.__format_df__()
        self.setup_tests()
    
    def setup_tests(self) -> None:
        self.header = "Ground Tests"
        if self.cfg.continuity_cfg.execute:
            self.tests.append(ContinuityTest(self.cfg.continuity_cfg))
        
    def __format_df__(self):
        grds = self.df["Ground"]
        first_element = grds[0]
        pairs = [[first_element, item] for item in grds[1:]]
        self.df = pd.DataFrame(pairs, columns=[FROM, TO])
        self.df[PIN_LEFT] = ""
        self.df[PIN_RIGHT] = ""
        