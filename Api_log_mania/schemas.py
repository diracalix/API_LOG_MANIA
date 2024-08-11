from pydantic import BaseModel
from datetime import datetime

class LogCreate(BaseModel):
    service_name: str
    log_level: str
    message: str

class LogResponse(BaseModel):
    id: int
    timestamp: datetime
    service_name: str
    log_level: str
    message: str
    received_at: datetime

    class Config:
        from_attributes = True  # Cambio en Pydantic V2
