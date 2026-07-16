from ai_service_api.schemas.prompts import PromptInspectionResponse


def calculate_prompt_metrics(prompt: str) -> PromptInspectionResponse:
    return PromptInspectionResponse(
        character_count=len(prompt),
        word_count=len(prompt.split()),
    )
