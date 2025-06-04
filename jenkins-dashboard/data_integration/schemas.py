from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

# This file is available for any shared Pydantic models within the
# data_integration component if it becomes more complex.
# For now, collector and parser define their main schemas internally
# or import from each other.

class ExampleSharedSchema(BaseModel):
    id: str
    description: Optional[str] = None
    data: Dict[str, Any]
