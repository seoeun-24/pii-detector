"""
2주차 작업 파일.

정규식으로 탐지된 '후보'가 실제 개인정보 문맥이 맞는지,
Gemini API를 호출해서 2차로 재판단하는 검증 로직.
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

    prompt = f"""문서에서 "{candidate}"라는 값 바로 앞에 붙은 라벨(이름표) 단어만 보고 판단하는 역할.
실제로 이 번호가 진짜 존재하는 사람의 정보인지는 신경X. 이건 테스트용 가상 문서라서 실존 여부는 판단 대상X.

오직 이 규칙만 적용:
- 값 바로 앞에 "연락처:", "휴대폰:", "전화:" 같은 라벨이 있으면 → 전화번호로 인정 (true)
- 값 바로 앞에 "이메일:", "메일:" 같은 라벨이 있으면 → 이메일로 인정 (true)
- 값 바로 앞에 "주민등록번호:" 라벨이 있으면 → 주민등록번호로 인정 (true)
- 값 바로 앞에 "외국인등록번호:" 라벨이 있으면 → 외국인등록번호로 인정 (true)
- 값 바로 앞에 "발주번호:", "일련번호:", "품목코드:" 처럼 다른 종류의 코드/번호 라벨이 있으면 → 오탐 (false)

문서 전체 내용:
\"\"\"{context}\"\"\"

판단 대상 값: "{candidate}"
이 값은 {type_name_kr}로 라벨링되어 있는가?

다른 설명 없이 JSON 한 줄로만 답해: {{"is_valid": true}} 또는 {{"is_valid": false}}"""

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
        print(f"[경고] LLM 응답 파싱 실패: {text!r}")
        return True  # 파싱 실패 시 정규식 결과를 그대로 신뢰 (보수적 처리)
