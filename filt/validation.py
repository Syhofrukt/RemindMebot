from pydantic import BaseModel
from typing import Optional
import time

class Remind(BaseModel):
    user_id: Optional[int]
    remind_name: Optional[str]
    remind_timedata: Optional[time.struct_time]
    user_timezone: Optional[str]

