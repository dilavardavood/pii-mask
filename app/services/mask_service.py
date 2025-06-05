import json

from app.services.llm_service import ask_openai
from app.utils.helper import extract_json
from app.utils.prompt_gallery import get_pii_prompt, get_pii_substitution_prompt


def mask_data(data, strictness="MEDIUM", mask_entity=None, substitute=False):
    input_data =json.dumps(data, indent=2)
    if substitute:
        pii_prompt = get_pii_substitution_prompt(strictness, entity=mask_entity)
    else:
        pii_prompt = get_pii_prompt(strictness, mask_entity=mask_entity)

    masked_data = ask_openai(pii_prompt,input_data,temperature=0.0)
    masked_data = extract_json(masked_data)
    print("Masked Data:", masked_data)
    return masked_data