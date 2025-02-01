import pandas as pd
import natsort as ns

from ..config_classes.config import *
from ..utils.labels import *

PIN_LEFT = WL.PIN_LEFT.value
PIN_RIGHT = WL.PIN_RIGHT.value
FROM = WL.FROM.value
TO = WL.TO.value
CONNECTOR = CL.CONNECTOR.value
PIN = CL.PIN.value

class BaseRoTest:

    """
    A class used to represent test types on Ditmco

    ...

    Attributes
    ----------
    cfg : TestConfig
        contains metadata about test parameters and etc.
    name : str
        str name test type

    Methods
    -------
    __to_input__(row: pd.Series)
        returns parsed row into input test str
    
    __convert__(df: pd.DataFrame)
        returns converted dataframe with input and/not output columns
    
    convert_to_test(df: pd.DataFrame)
        returns test str formatted with in testing block format
    """

    def __init__(self, cfg: TestConfig):
        self.cfg: TestConfig = cfg
        self.name: str = None

    def __to_input__(self, row: pd.Series) -> str:
        pass

    def __convert__(self, df: pd.DataFrame) -> pd.DataFrame:
        pass

    def convert_to_test(self, df: pd.DataFrame) -> str:
        leakage_df = self.__convert__(df)
        header = f"BTB, {self.cfg.block_name}\n" + self.cfg.params + "\n"
        footer = f"ETB, {self.cfg.block_name}\n"
        return header + leakage_df[self.name].aggregate("sum", axis=0) + footer

class ContinuityTest(BaseRoTest):

    def __init__(self, conf: TestConfig):
        super().__init__(conf)
        self.name = "continuity"

    def __to_output__(self, row: pd.Series) -> str:
        pin = "-" + str(row[PIN_LEFT]) + "\n" if row[PIN_LEFT] != "" else "\n"
        return "X-" + str(row[FROM]) + pin

    def __to_input__(self, row: pd.Series) -> str:
        pin =  "-" + str(row[PIN_RIGHT]) + "\n" if row[PIN_RIGHT] != "" else "\n"
        return "C-" + str(row[TO]) + pin
    
    def __to_input_group__(self, group: pd.DataFrame) -> pd.Series:
        if len(group) > 1:
            sorted_cont_pts = pd.Series(ns.natsorted(group.apply(self.__to_multiple_continuity__, axis=1)))
            sorted_cont_pts.iloc[-1] = sorted_cont_pts.iloc[-1].replace("CV-", "C-")
            return pd.Series(sorted_cont_pts.agg("sum"))
        return group.apply(self.__to_input__, axis=1).reset_index(drop=True)
            
    def __to_multiple_continuity__(self, row: pd.Series) -> str:
        pin = "-" + str(row[PIN_RIGHT]) + "\n" if row[PIN_RIGHT] != "" else "\n"
        return "CV-" + str(row[TO]) + pin

    def __convert__(self, df: pd.DataFrame) -> pd.DataFrame:
        cont_df = df.copy()
        cont_df["output"] = cont_df.apply(self.__to_output__, axis=1)
        cont_df = cont_df.groupby("output").apply(self.__to_input_group__, include_groups=False).reset_index().rename(columns={0:"input"})
        cont_df[self.name] = pd.Series(ns.natsorted(cont_df.apply("sum", axis=1)))
        return cont_df
    
class HipotTest(BaseRoTest):

    def __init__(self, conf: TestConfig):
        super().__init__(conf)
        self.name = "hipot"

    def __to_input__(self, row: pd.Series) -> str:
        return "D-" + str(row[CONNECTOR]) + "-" + str(row[PIN]) + "\n"

    def __convert__(self, df: pd.DataFrame) -> pd.DataFrame:
        left = df[[FROM, PIN_LEFT]].rename(columns={FROM: CONNECTOR, PIN_LEFT: PIN})
        right = df[[TO, PIN_RIGHT]].rename(columns={TO: CONNECTOR, PIN_RIGHT: PIN})
        connectors = pd.concat([left, right], ignore_index=True).drop_duplicates(subset=[CONNECTOR, PIN])
        sorted_con_pin = ns.natsorted(connectors.apply(self.__to_input__, axis=1))
        return pd.DataFrame({self.name: sorted_con_pin})

class IsolationTest(BaseRoTest):

    def __init__(self, conf: TestConfig):
        super().__init__(conf)
        self.name = "isolation"

    def __to_input__(self, row: pd.Series) -> str:
        return "T-" + str(row[CONNECTOR]) + "-" + str(row[PIN]) + "\n"

    def __convert__(self, df: pd.DataFrame) -> pd.DataFrame:
        sorted_con_pin = ns.natsorted(df.apply(self.__to_input__, axis=1))
        return pd.DataFrame({self.name: sorted_con_pin})

class LeakageTest(BaseRoTest):

    def __init__(self, conf: TestConfig):
        super().__init__(conf)
        self.name = "leakage"

    def __to_input__(self, row: pd.Series) -> str:
        return "F-" + str(row[CONNECTOR]) + "-" + str(row[PIN]) + "\n"
    
    def __convert__(self, df: pd.DataFrame) -> pd.DataFrame:
        left = df[[FROM, PIN_LEFT]].rename(columns={FROM: CONNECTOR, PIN_LEFT: PIN})
        right = df[[TO, PIN_RIGHT]].rename(columns={TO: CONNECTOR, PIN_RIGHT: PIN})
        connectors = pd.concat([left, right], ignore_index=True).drop_duplicates(subset=[CONNECTOR, PIN])
        sorted_con_pin = ns.natsorted(connectors.apply(self.__to_input__, axis=1))
        return pd.DataFrame({self.name: sorted_con_pin})