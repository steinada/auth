from pydantic import BaseModel, Field


class PageFilter(BaseModel):
    limit: int = Field(ge=5)
    page: int = Field(ge=0)
    sort_by: dict = Field(default=dict(), examples=[{'name': 'desc'}])
