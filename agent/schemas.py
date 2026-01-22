from typing import List, Optional, Union
from pydantic import BaseModel
from datetime import datetime

class Action(BaseModel):
    type: str
    selector: Optional[str] = None
    value: Optional[Union[str, int]] = None  # Accept both string and int
    description: Optional[str] = None  # Human-readable description

class Plan(BaseModel):
    actions: List[Action]

class ExecutionStepResult(BaseModel):
    action: Action
    success: bool
    error: Optional[str] = None
    screenshot_path: Optional[str] = None
    timestamp: str = ""
    execution_time_ms: int = 0
    
    def __init__(self, **data):
        if 'timestamp' not in data or not data['timestamp']:
            data['timestamp'] = datetime.now().isoformat()
        super().__init__(**data)
