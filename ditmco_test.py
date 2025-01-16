import pandas as pd
from config_classes.config import Config
from converter.ro_tests import *

class DitmcoTest:

    def __init__(self, cfg: Config):
        self.cfg = cfg
        self.df = pd.read_csv(cfg.csv_path)
    
    def produce_test(self):
        tests = []
        if self.cfg.continuity:
            tests.append(ContinuityTest(self.cfg.continuity_cfg))
        if self.cfg.isolation:
            tests.append(IsolationTest(self.cfg.isolation_cfg))
        if self.cfg.hipot:
            tests.append(HipotTest(self.cfg.hipot_cfg))
        self.__combine_tests__(tests=tests)

    def __combine_tests__(self, tests: list[BaseTest]):
        final_test = ""
        for test in tests:
            final_test += test.convert_to_test()
        return final_test
    
    def save_as(self, test_str):
        with open(self.cfg.file_name, "w") as file:
            file.write(test_str)