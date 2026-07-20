"""
1week, 2ndweek 작업 파일

PII 유형별 정규표현식 패턴을 정의

각 함수는 텍스트를 입력받아 탐지된 (매칭된 문자열, 시작위치, 끝위치) 리스트를 반환
"""


import re


def detect_phone(text: str) -> list[tuple[str, int, int]]:
    """전화번호 탐지. 예: 010-1234-5678, 01012345678"""
    pattern = r"01[016789]-?\d{3,4}-?\d{4}"
    results = []
    for match in re.finditer(pattern, text):
        results.append((match.group(), match.start(), match.end()))
    return results


def detect_email(text: str) -> list[tuple[str, int, int]]:
    """이메일 탐지. 예: example@domain.com"""
    pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    results = []
    for match in re.finditer(pattern, text):
        results.append((match.group(), match.start(), match.end()))
    return results


def detect_rrn(text: str) -> list[tuple[str, int, int]]:
    """
    주민등록번호 탐지. 예: 900101-1234567
    뒷자리 첫 숫자: 1,2,3,4 (내국인) — 체크섬 검증은 이번 범위에서 제외.
    정규식으로는 형식만 잡고, 월/일 범위는 파이썬 코드로 검증.
    """
    pattern = r"\d{6}-[1234]\d{6}"
    results = []
    for match in re.finditer(pattern, text):
        candidate = match.group()
        month = int(candidate[2:4])
        day = int(candidate[4:6])
        if 1 <= month <= 12 and 1 <= day <= 31:
            results.append((candidate, match.start(), match.end()))
    return results


def detect_foreigner_id(text: str) -> list[tuple[str, int, int]]:
    """
    외국인등록번호 탐지. 예: 900101-5234567
    뒷자리 첫 숫자: 5,6,7,8 (외국인) — RRN과 동일한 로직, 뒷자리 범위만 다름.
    """
    pattern = r"\d{6}-[5678]\d{6}"
    results = []
    for match in re.finditer(pattern, text):
        candidate = match.group()
        month = int(candidate[2:4])
        day = int(candidate[4:6])
        if 1 <= month <= 12 and 1 <= day <= 31:
            results.append((candidate, match.start(), match.end()))
    return results


# 유형명 -> 탐지 함수 매핑 (scanner.py에서 이걸 순회하며 사용)
PII_DETECTORS = {
    "phone": detect_phone,
    "email": detect_email,
    "rrn": detect_rrn,
    "foreigner_id": detect_foreigner_id,
}