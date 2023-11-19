from dataclasses import dataclass
from typing import Callable, List
from dataclasses import dataclass, field
import time


@dataclass
class chat:
    from_name: str
    to_name: str