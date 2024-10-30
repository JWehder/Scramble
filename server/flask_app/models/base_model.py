from bson import ObjectId
from pydantic import BaseModel

class Base(BaseModel):
    def to_dict(self):
        # Convert ObjectId to string and create a dictionary
        data = self.dict()
        for key, value in data.items():
            if isinstance(value, ObjectId):
                data[key] = str(value)
        return data