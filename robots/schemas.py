from pydantic import BaseModel
from pydantic import ConfigDict


class RobotInfo(BaseModel):
    serial: str
    model: str
    version: str
    model_config = ConfigDict(from_attributes=True)


class RobotToExcel(BaseModel):
    model: str
    version: str
    total: int
    model_config = ConfigDict(from_attributes=True)
