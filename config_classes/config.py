from dataclasses import dataclass
from typing import Optional, Union

@dataclass
class TestConfig:
    block_name: str
    param: str

@dataclass
class Config:
    results_path: str
    wire_list_path: str
    unused_pins_path: str
    ground_path: str

    continuity: bool
    isolation: bool
    hipot: bool

    continuity_cfg: TestConfig
    isolation_cfg: TestConfig
    hipot_cfg: TestConfig