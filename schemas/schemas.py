import re
from pydantic import BaseModel, Field, EmailStr, validator


class Comment(BaseModel):
    comment: str 

    @validator('comment')
    def username_validator(cls, v):
        if not 1 < len(v) < 500:
            raise ValueError('Comment must contain between 1 and 500 letters')
        return v
    



