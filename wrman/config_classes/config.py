from dataclasses import dataclass
from typing import Optional, Union

@dataclass
class TestConfig:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    execute: True
    block_name: str
    param: str

@dataclass
class Config:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if isinstance(value, dict):
                setattr(self, key, TestConfig(**value))  # Convert dict to OK object
            else:
                setattr(self, key, value)
                
    results_path: str
    continuity_cfg: TestConfig
    leakage_cfg: TestConfig
    isolation_cfg: TestConfig
    hipot_cfg: TestConfig