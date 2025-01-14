import pandas as pd
import natsort as ns

class BaseTest:

    def __init__(self, block_name: str, params: str):
        self.block_name = block_name
        self.params = params

    def __to_input__(self) -> str:
        pass

    def __convert__(self) -> pd.DataFrame:
        pass

    def convert_to_test(self) -> str:
        pass

class ContinuityTest(BaseTest):

    def __init__(self, block_name: str, params: str):
        super().__init__(block_name, params)

    def to_output(row) -> str:
        pin = "-" + str(row["PIN LEFT"]) + "\n" if row["PIN LEFT"] != "" else "\n"
        return "\nX-" + str(row["FROM"]) + pin

    def __to_input__(self, row) -> str:
        pin =  "-" + str(row["PIN RIGHT"]) + "\n" if row["PIN RIGHT"] != "" else "\n"
        return "C-" + str(row["TO"]) + pin
    
    def to_input_group(self, group):
        if len(group) > 1:
            sorted_cont_pts = pd.Series(ns.natsorted(group.apply(self.to_multiple_continuity, axis=1)))
            sorted_cont_pts.iloc[-1] = sorted_cont_pts.iloc[-1].replace("CV-", "C-")
            return pd.Series(sorted_cont_pts.agg("sum"))
        return group.apply(self.__to_input__, axis=1)
            
    def to_multiple_continuity(self, row) -> str:
        pin = "-" + str(row["PIN RIGHT"]) + "\n" if row["PIN RIGHT"] != "" else "\n"
        return "CV-" + str(row["TO"]) + pin

    def __convert__(self, df: pd.DataFrame) -> pd.DataFrame:
        cont_df = df.copy()
        cont_df["output"] = cont_df.apply(self.to_output, axis=1)
        cont_df = cont_df.groupby("output").apply(self.to_input_continuity, include_groups=False).reset_index(name="input").drop("level_1", axis=1)
        cont_df["continuity"] = pd.Series(ns.natsorted(cont_df.apply("sum", axis=1)))
        return cont_df

    def convert_to_test(self, df: pd.DataFrame) -> str:
        cont_df = self, self.convert_continuity(df)
        header = f"BTB, {self.block_name}\n" + self.params + "\n"
        footer = f"\nETB, {self.block_name}\n"
        return header + cont_df["continuity"].aggregate("sum", axis=0) + footer
    
class HipotTest(BaseTest):

    def __init__(self, block_name: str, params: str):
        super().__init__(block_name, params)

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


class IsolationTest(BaseTest):

    def __init__(self, block_name: str, params: str):
        super().__init__(block_name, params)

    def __to_input__(self, row):
        return "\nD-" + str(row["Connector"]) + "-" + str(row["Pin"]) + "\n"

    def __convert__(self, df: pd.DataFrame):
        left = df[['FROM', 'PIN LEFT']].rename(columns={'FROM': "Connector", "PIN LEFT": "Pin"})
        right = df[['TO', 'PIN RIGHT']].rename(columns={'TO': "Connector", "PIN RIGHT": "Pin"})
        connectors = pd.concat([left, right], ignore_index=True).drop_duplicates(subset=['Connector', 'Pin'])
        column_name = "hipot"
        sorted_con_pin = ns.natsorted(connectors.apply(self.__to_input__, axis=1))
        return pd.DataFrame({column_name: sorted_con_pin})

    def convert_to_test(self, df: pd.DataFrame, block_name: str, params: str):
        hipot_df = self.__convert__(df)
        header = f"BTB, {block_name}\n" + params + "\n"
        footer = f"ETB, {block_name}\n"
        return header + hipot_df["hipot"].aggregate("sum", axis=0) + footer