from pydantic import BaseModel
from pydantic import ConfigDict


class RobotBase(BaseModel):
    serial: str
    model: str
    version: str
    model_config = ConfigDict(from_attributes=True)
