from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime




class UserIn(BaseModel):
    username: str = Field(min_length=4, max_length=15)
    password: str = Field(min_length=10, max_length=30)



class UserOut(BaseModel):
    id: int
    username: str
    registered_at: datetime

    model_config: ConfigDict = ConfigDict(from_attributes=True)

