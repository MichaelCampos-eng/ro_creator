import pandas as pd
import natsort as ns

from ..config_classes.config import *

class BaseRoTest:

    def __init__(self, conf: TestConfig):
        self.conf = conf

    def __to_input__(self, row) -> str:
        pass

    def __convert__(self, df: pd.DataFrame) -> pd.DataFrame:
        pass

    def convert_to_test(self, df: pd.DataFrame) -> str:
        pass

class ContinuityTest(BaseRoTest):

    def __init__(self, conf: TestConfig):
        super().__init__(conf)

    def __to_output__(row) -> str:
        pin = "-" + str(row["PIN LEFT"]) + "\n" if row["PIN LEFT"] != "" else "\n"
        return "\nX-" + str(row["FROM"]) + pin

    def __to_input__(self, row) -> str:
        pin =  "-" + str(row["PIN RIGHT"]) + "\n" if row["PIN RIGHT"] != "" else "\n"
        return "C-" + str(row["TO"]) + pin
    
    def __to_input_group__(self, group) -> pd.Series:
        if len(group) > 1:
            sorted_cont_pts = pd.Series(ns.natsorted(group.apply(self.to_multiple_continuity, axis=1)))
            sorted_cont_pts.iloc[-1] = sorted_cont_pts.iloc[-1].replace("CV-", "C-")
            return pd.Series(sorted_cont_pts.agg("sum"))
        return group.apply(self.__to_input__, axis=1).reset_index(drop=True)
            
    def __to_multiple_continuity__(self, row) -> str:
        pin = "-" + str(row["PIN RIGHT"]) + "\n" if row["PIN RIGHT"] != "" else "\n"
        return "CV-" + str(row["TO"]) + pin

    def __convert__(self, df: pd.DataFrame) -> pd.DataFrame:
        cont_df = df.copy()
        cont_df["output"] = cont_df.apply(self.__to_output__, axis=1)
        cont_df = cont_df.groupby("output").apply(self.__to_input_group__, include_groups=False).reset_index().rename(columns={0:"input"})
        cont_df["continuity"] = pd.Series(ns.natsorted(cont_df.apply("sum", axis=1)))
        return cont_df

    def convert_to_test(self, df: pd.DataFrame) -> str:
        cont_df = self, self.convert_continuity(df)
        header = f"BTB, {self.block_name}\n" + self.params + "\n"
        footer = f"\nETB, {self.block_name}\n"
        return header + cont_df["continuity"].aggregate("sum", axis=0) + footer
    
class HipotTest(BaseRoTest):

    def __init__(self, conf: TestConfig):
        super().__init__(conf)

    def __to_input__(self, row) -> str:
        return "\nD-" + str(row["Connector"]) + "-" + str(row["Pin"]) + "\n"

    def __convert__(self, df: pd.DataFrame) -> pd.DataFrame:
        left = df[['FROM', 'PIN LEFT']].rename(columns={'FROM': "Connector", "PIN LEFT": "Pin"})
        right = df[['TO', 'PIN RIGHT']].rename(columns={'TO': "Connector", "PIN RIGHT": "Pin"})
        connectors = pd.concat([left, right], ignore_index=True).drop_duplicates(subset=['Connector', 'Pin'])
        column_name = "hipot"
        sorted_con_pin = ns.natsorted(connectors.apply(self.__to_input__, axis=1))
        return pd.DataFrame({column_name: sorted_con_pin})

    def convert_to_test(self, df: pd.DataFrame, block_name: str, params: str) -> str:
        hipot_df = self.__convert__(df)
        header = f"BTB, {block_name}\n" + params + "\n"
        footer = f"ETB, {block_name}\n"
        return header + hipot_df["hipot"].aggregate("sum", axis=0) + footer

# TODO: Df for isolation would only be connector and pin columns
class IsolationTest(BaseRoTest):

    def __init__(self, conf: TestConfig):
        super().__init__(conf)

    def __to_input__(self, row) -> str:
        return "\nT-" + str(row["Connector"]) + "-" + str(row["Pin"]) + "\n"

    def __convert__(self, df: pd.DataFrame) -> pd.DataFrame:
        left = df[['FROM', 'PIN LEFT']].rename(columns={'FROM': "Connector", "PIN LEFT": "Pin"})
        right = df[['TO', 'PIN RIGHT']].rename(columns={'TO': "Connector", "PIN RIGHT": "Pin"})
        connectors = pd.concat([left, right], ignore_index=True).drop_duplicates(subset=['Connector', 'Pin'])
        column_name = "hipot"
        sorted_con_pin = ns.natsorted(connectors.apply(self.__to_input__, axis=1))
        return pd.DataFrame({column_name: sorted_con_pin})

    def convert_to_test(self, df: pd.DataFrame, block_name: str, params: str) -> str:
        hipot_df = self.__convert__(df)
        header = f"BTB, {block_name}\n" + params + "\n"
        footer = f"ETB, {block_name}\n"
        return header + hipot_df["hipot"].aggregate("sum", axis=0) + footer

class LeakageTest(BaseRoTest):

    def __init__(self, conf: TestConfig):
        super().__init__(conf)

    def __to_input__(self, row) -> str:
        return "\nF-" + str(row["Connector"]) + "-" + str(row["Pin"]) + "\n"
    
    def __convert__(self, df: pd.DataFrame) -> pd.DataFrame:
        left = df[['FROM', 'PIN LEFT']].rename(columns={'FROM': "Connector", "PIN LEFT": "Pin"})
        right = df[['TO', 'PIN RIGHT']].rename(columns={'TO': "Connector", "PIN RIGHT": "Pin"})
        connectors = pd.concat([left, right], ignore_index=True).drop_duplicates(subset=['Connector', 'Pin'])
        column_name = "leakage"
        sorted_con_pin = ns.natsorted(connectors.apply(self.__to_input__, axis=1))
        return pd.DataFrame({column_name: sorted_con_pin})

    def convert_to_test(self, df: pd.DataFrame, block_name: str, params: str) -> str:
        leakage_df = self.__convert__(df)
        header = f"BTB, {block_name}\n" + params + "\n"
        footer = f"ETB, {block_name}\n"
        return header + leakage_df["hipot"].aggregate("sum", axis=0) + footer