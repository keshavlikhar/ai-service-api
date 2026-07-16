from fastapi import APIRouter

from ai_service_api.schemas.prompts import (
    PromptInspectionRequest,
    PromptInspectionResponse,
)
from ai_service_api.services.prompts import calculate_prompt_metrics

router = APIRouter(
    prefix="/v1/prompts",
    tags=["prompts"],
)


@router.post(
    "/inspect",
    response_model=PromptInspectionResponse,
)
def inspect_prompt(
    request: PromptInspectionRequest,
) -> PromptInspectionResponse:
    return calculate_prompt_metrics(request.prompt)
