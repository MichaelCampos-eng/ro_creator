from dataclasses import dataclass
from typing import Optional

@dataclass
class TestConfig:
    task: str
    file_test_name: str
    file_test_mode: str
    file_location: Optional[str]
    test_param: str
    unused_pins: str
    wire_list: str

class Config:
    tests: str