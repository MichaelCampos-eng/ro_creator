from dataclasses import dataclass

@dataclass
class TestConfig:
    execute: True
    block_name: str
    params: str

    def update_execute(self, execute):
        self.execute = execute
    
    def update_block_name(self, block_name):
        self.block_name = block_name

    def update_params(self, params):
        self.params = params

@dataclass
class Config:
    results_path: str
    continuity_cfg: TestConfig
    leakage_cfg: TestConfig
    isolation_cfg: TestConfig
    hipot_cfg: TestConfig
