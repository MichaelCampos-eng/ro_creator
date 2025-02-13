from ..converter.ro_tests import *
import pandas as pd
from typing import List
from ..utils.labels import *
from ..conn_management.table import DataEntryManager

PIN_LEFT = WL.PIN_LEFT.value
PIN_RIGHT = WL.PIN_RIGHT.value
FROM = WL.FROM.value
TO = WL.TO.value
GROUND = CL.GROUND.value

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
    __setup_tests__()
        creates instances of RO tests and appends it to tests according to cfg
    
    execute()
        if df is not empty, return str of all ro tests based on tests attribute
    """

    def __init__(self, list: DataEntryManager, cfg: Config):
        self.manager = list
        self.cfg = cfg
        self.tests: List[BaseRoTest] = []
        self.header = ""
    
    def __setup_tests__(self) -> None:
        pass
    
    def __get_df_formatted__(self) -> pd.DataFrame:
        return self.manager.get_df()

    def execute(self) -> str:
        if not self.manager.is_df_empty():
            return f"; {self.header}\n" + "".join([test.convert_to_test(self.__get_df_formatted__()) + "\n" for test in self.tests])
        raise ValueError("Dataframe is empty.")
    

class WireListTest(BaseListTest):

    def __init__(self, list: DataEntryManager, cfg: Config):
        super().__init__(list, cfg)
        self.__setup_tests__()
    
    def __setup_tests__(self) -> None:
        self.header = "Wire List Tests"
        if self.cfg.continuity_cfg.execute:
            self.tests.append(ContinuityTest(self.cfg.continuity_cfg))
        if self.cfg.leakage_cfg.execute:
            self.tests.append(LeakageTest(self.cfg.leakage_cfg))
        if self.cfg.hipot_cfg.execute:
            self.tests.append(HipotTest(self.cfg.hipot_cfg)) 

class UnusedListTest(BaseListTest):

    def __init__(self, list: DataEntryManager, cfg: Config):
        super().__init__(list, cfg)
        self.__setup_tests__()
    
    def __setup_tests__(self) -> None:
        self.header = "Unused Pins Tests"
        if self.cfg.isolation_cfg.execute:
            self.tests.append(IsolationTest(self.cfg.isolation_cfg))

class GroundListTest(BaseListTest):

    def __init__(self, list: DataEntryManager, cfg: Config):
        super().__init__(list, cfg)
        self.__setup_tests__()
    
    def __setup_tests__(self) -> None:
        self.header = "Ground Tests"
        if self.cfg.continuity_cfg.execute:
            self.tests.append(ContinuityTest(self.cfg.continuity_cfg))
    
    def execute(self):
        if len(self.manager.get_df().index) > 1:
            return super().execute()
        else:
            raise ValueError("There must be at least 2 ground connectors for continuity test.")      

    def __get_df_formatted__(self):
        df = self.manager.get_df()
        grds = df[GROUND]
        first_element = grds[0]
        pairs = [[first_element, item] for item in grds[1:]]
        df = pd.DataFrame(pairs, columns=[FROM, TO])
        df[PIN_LEFT] = ""
        df[PIN_RIGHT] = ""
        return df
            