from pydantic import BaseModel, Field, field_validator


class PromptInspectionRequest(BaseModel):
    prompt: str = Field(min_length=1, max_length=10_000)

    @field_validator("prompt")
    @classmethod
    def prompt_must_not_be_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Prompt must not be blank")
        return value


class PromptInspectionResponse(BaseModel):
    character_count: int = Field(ge=0)
    word_count: int = Field(ge=0)
