"""API 키가 잘 연결되는지 딱 한 번만 확인해보는 용도"""
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from src.llm_verifier import verify_candidate

result = verify_candidate(
    context="발주번호: 123456-1234567, 품목: 사무용품",
    candidate="123456-1234567",
    pii_type="rrn",
)
print(f"판단 결과: {result}")  # False가 나오면 성공 (발주번호를 주민번호 아니라고 잘 걸러낸 것)