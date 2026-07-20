"""
1주차 작업 파일.

patterns.py의 각 탐지 함수가 정확한지 확인하는 단위 테스트.
정규식 하나 짤 때마다 여기에 테스트 케이스를 추가하면서 검증하는 걸 추천.

실행 방법: (가상환경 활성화된 상태에서)
    pytest tests/test_patterns.py -v
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from src.patterns import detect_phone, detect_email, detect_rrn, detect_foreigner_id


def test_detect_phone_basic():
    text = "연락처는 010-1234-5678 입니다."
    result = detect_phone(text)
    assert len(result) == 1
    assert result[0][0] == "010-1234-5678"


def test_detect_phone_no_hyphen():
    text = "연락처는 01012345678 입니다."
    result = detect_phone(text)
    assert len(result) == 1


def test_detect_email_basic():
    text = "이메일: test@example.com 로 보내주세요."
    result = detect_email(text)
    assert len(result) == 1
    assert result[0][0] == "test@example.com"


def test_detect_no_false_positive_on_normal_number():
    """일반적인 4자리 숫자(사번 등)를 전화번호로 오탐하지 않는지 확인"""
    text = "담당자 사번은 1234 입니다."
    result = detect_phone(text)
    assert len(result) == 0


# TODO: detect_rrn, detect_foreigner_id 테스트 케이스 추가
