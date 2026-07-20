"""

Week 2 implementation.

Validates whether candidates detected by regular expressions
are actual PII based on their surrounding context by calling
the Gemini API for a second-stage verification.

"""

import os
import json
from dotenv import load_dotenv
from google import genai

load_dotenv()  # .env 파일에서 GEMINI_API_KEY를 읽어온다

_client = None


def get_client():
    """API 클라이언트를 한 번만 만들어서 재사용 (매번 새로 만들 필요 없음)"""
    global _client
    if _client is None:
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise EnvironmentError("GEMINI_API_KEY 환경변수가 설정되지 않았습니다. .env 파일을 확인하세요.")
        _client = genai.Client(api_key=api_key)
    return _client


def verify_candidate(context: str, candidate: str, pii_type: str) -> bool:
    """
    context: 후보가 등장한 파일 전체 텍스트
    candidate: 정규식이 찾아낸 후보 문자열
    pii_type: "phone" / "email" / "rrn" / "foreigner_id"

    반환: True면 "진짜 개인정보로 판단", False면 "오탐으로 판단"
    """
    type_name_kr = {
        "phone": "전화번호",
        "email": "이메일",
        "rrn": "주민등록번호",
        "foreigner_id": "외국인등록번호",
    }.get(pii_type, pii_type)

    prompt = f"""
You are a PII validation assistant.

Your task is to determine whether the value "{candidate}" is labeled as a {type_name_en}
based solely on the label immediately preceding it.

Do NOT determine whether the value belongs to a real person.
This is a synthetic test document, so the authenticity or existence of the value is irrelevant.

Apply ONLY the following rules:

- If the label immediately before the value is "Contact:", "Mobile:", or "Phone:", return true.
- If the label is "Email:" or "E-mail:", return true.
- If the label is "Resident Registration Number:", return true.
- If the label is "Foreigner Registration Number:", return true.
- If the label indicates another type of identifier, such as "Order Number:", "Serial Number:", or "Product Code:", return false.

Document:

\"\"\"{context}\"\"\"

Candidate value:
"{candidate}"

Is this value labeled as a {type_name_en}?

Respond with exactly one JSON object and nothing else.

{{"is_valid": true}}

or

{{"is_valid": false}}
"""

client = get_client()

from google.genai import types

response = client.models.generate_content(
    model="gemini-flash-lite-latest",
    contents=prompt,
    config=types.GenerateContentConfig(
        response_mime_type="application/json",
        temperature=0,
    ),
)

text = response.text.strip()

try:
    result = json.loads(text)
    return bool(result.get("is_valid", False))
except json.JSONDecodeError:
    print(f"[Warning] Failed to parse LLM response: {text!r}")
    # Fall back to the regex result if the response cannot be parsed.
    return True
