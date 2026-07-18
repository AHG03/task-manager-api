from pydantic import BaseModel, ConfigDict, StringConstraints
from typing import Annotated


class MessageResponse(BaseModel):
    message: str


class TaskBase(BaseModel):
    title: Annotated[str, StringConstraints(
        strip_whitespace=True, min_length=1)]


class TaskCreate(TaskBase):
    pass


class TaskUpdate(TaskBase):
    completed: bool


class TaskResponse(TaskBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    completed: bool


class TaskPatch(BaseModel):
    title: Annotated[str | None, StringConstraints(
        strip_whitespace=True, min_length=1)] = None
    completed: bool | None = None
