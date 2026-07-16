from pydantic import BaseModel, Field


class PromptInspectionRequest(BaseModel):
    prompt: str = Field(min_length=1, max_length=10_000)


class PromptInspectionResponse(BaseModel):
    character_count: int = Field(ge=0)
    word_count: int = Field(ge=0)
