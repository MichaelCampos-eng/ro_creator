from dataclasses import dataclass
from typing import Optional, Union

@dataclass
class TestConfig:
    execute: True
    block_name: str
    params: str

@dataclass
class Config:
    results_path: str
    continuity_cfg: TestConfig
    leakage_cfg: TestConfig
    isolation_cfg: TestConfig
    hipot_cfg: TestConfig