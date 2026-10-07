from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, model_validator
class AssetCreate(BaseModel):
    asset_tag: str = Field(min_length=1, max_length=40, pattern=r"^[A-Z0-9-]+$")
    name: str = Field(min_length=1, max_length=160)
    category: str = Field(min_length=1, max_length=50)
    description: str = Field(default="", max_length=2000)
    total: int = Field(ge=1, le=1000)
class AssetUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=160)
    category: str | None = Field(default=None, min_length=1, max_length=50)
    description: str | None = Field(default=None, max_length=2000)
    total: int | None = Field(default=None, ge=1, le=1000)
    @model_validator(mode="before")
    @classmethod
    def no_explicit_nulls(cls, data):
        if isinstance(data, dict) and any(v is None for v in data.values()):
            raise ValueError("Supplied fields cannot be null")
        return data
class AssetOut(AssetCreate):
    id: int
    available: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
class BorrowCreate(BaseModel):
    asset_id: int = Field(gt=0)
    borrower: str = Field(min_length=1, max_length=100)
    quantity: int = Field(default=1, ge=1, le=100)
class LoanOut(BaseModel):
    id: int
    asset_id: int
    asset_name: str
    borrower: str
    quantity: int
    borrowed_at: datetime
    returned_at: datetime | None
    model_config = ConfigDict(from_attributes=True)
