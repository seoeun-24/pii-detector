"""
2주차 작업 파일.

더미(가상) PII 데이터가 섞인 테스트 파일을 자동으로 대량 생성한다.
실제 개인정보는 전혀 사용하지 않는다.

이번 버전은 "함정 케이스"를 포함한다:
  - hard_*.txt: 진짜 PII이지만 형식이 까다로워(공백 구분 등) 정규식이 놓칠 수 있는 경우 (미탐 유도)
  - trap_*.txt: PII처럼 생겼지만 실제로는 사내 코드(발주번호 등)인 경우 (오탐 유도)

동시에 "정답 라벨"(ground_truth.json)도 같이 만들어서, evaluator.py에서
Precision/Recall 계산할 때 기준값으로 쓴다.
"""

import random
import json
from pathlib import Path

OUTPUT_DIR = Path("test_files/generated")
GROUND_TRUTH_PATH = Path("test_files/ground_truth.json")

random.seed(42)  # 매번 같은 결과가 나오게 고정 (재현성)

FIRST_NAMES = ["민준", "서연", "지호", "하은", "도윤", "지민", "예은", "시우"]
LAST_NAMES = ["김", "이", "박", "최", "정", "강", "조", "윤"]


def random_phone():
    prefix = random.choice(["010", "011", "016", "017", "018", "019"])
    mid = random.randint(1000, 9999)
    end = random.randint(1000, 9999)
    return f"{prefix}-{mid}-{end}"


def random_phone_spaced():
    """하이픈 대신 공백으로 구분된 전화번호 (현재 정규식은 못 잡음 → 미탐 유도)"""
    prefix = random.choice(["010", "011", "016", "017", "018", "019"])
    mid = random.randint(1000, 9999)
    end = random.randint(1000, 9999)
    return f"{prefix} {mid} {end}"


def random_email():
    name = random.choice(["kim", "lee", "park", "choi", "test", "hong"])
    num = random.randint(1, 999)
    domain = random.choice(["gmail.com", "naver.com", "company.co.kr", "test.com"])
    return f"{name}{num}@{domain}"


def random_rrn():
    yy = random.randint(0, 99)
    mm = random.randint(1, 12)
    dd = random.randint(1, 28)
    gender = random.choice([1, 2, 3, 4])
    rest = random.randint(100000, 999999)
    return f"{yy:02d}{mm:02d}{dd:02d}-{gender}{rest}"


def random_rrn_no_hyphen():
    """하이픈 없이 13자리로 붙여쓴 주민등록번호 (현재 정규식은 못 잡음 → 미탐 유도)"""
    yy = random.randint(0, 99)
    mm = random.randint(1, 12)
    dd = random.randint(1, 28)
    gender = random.choice([1, 2, 3, 4])
    rest = random.randint(100000, 999999)
    return f"{yy:02d}{mm:02d}{dd:02d}{gender}{rest}"


def random_foreigner_id():
    yy = random.randint(0, 99)
    mm = random.randint(1, 12)
    dd = random.randint(1, 28)
    gender = random.choice([5, 6, 7, 8])
    rest = random.randint(100000, 999999)
    return f"{yy:02d}{mm:02d}{dd:02d}-{gender}{rest}"


def random_trap_code():
    """
    PII처럼 생겼지만 실제로는 사내 발주번호/일련번호인 값.
    RRN 정규식(\\d{6}-[1234]\\d{6})과 형식이 완전히 똑같아서
    정규식이 오탐(false positive)하게 되는 함정.
    """
    part1 = random.randint(100000, 999999)
    gender_like = random.choice([1, 2, 3, 4])
    part2 = random.randint(100000, 999999)
    return f"{part1}-{gender_like}{part2}"


def random_name():
    return random.choice(LAST_NAMES) + random.choice(FIRST_NAMES)


def generate_pii_file(index: int) -> dict:
    """PII가 포함된 더미 파일 (깔끔한 형식). 정답 라벨도 같이 반환."""
    templates = [
        "고객 문의 메모\n담당자: {name}\n연락처: {phone}\n이메일: {email}\n",
        "회원 가입 정보\n이름: {name}\n휴대폰: {phone}\n주민등록번호: {rrn}\n",
        "외국인 고객 응대 기록\n이름: {name}\n외국인등록번호: {fid}\n연락처: {phone}\n",
        "메일 발송 이력\n수신자: {email}\n담당자 연락처: {phone}\n",
    ]

    template = random.choice(templates)
    phone = random_phone()
    email = random_email()
    rrn = random_rrn()
    fid = random_foreigner_id()
    name = random_name()

    content = template.format(name=name, phone=phone, email=email, rrn=rrn, fid=fid)

    ground_truth = {"phone": [], "email": [], "rrn": [], "foreigner_id": []}
    if "{phone}" in template:
        ground_truth["phone"].append(phone)
    if "{email}" in template:
        ground_truth["email"].append(email)
    if "{rrn}" in template:
        ground_truth["rrn"].append(rrn)
    if "{fid}" in template:
        ground_truth["foreigner_id"].append(fid)

    filename = f"dummy_{index:03d}.txt"
    return {"filename": filename, "content": content, "ground_truth": ground_truth}


def generate_hard_pii_file(index: int) -> dict:
    """
    진짜 PII가 들어있지만, 형식이 까다로워서(공백 구분, 하이픈 없음)
    현재 정규식이 놓칠 가능성이 있는 파일. → 미탐(FN) 유도용.
    """
    templates = [
        "메모\n{name} 고객님 연락처 {phone_spaced} 로 회신 요망\n",
        "신원 확인 서류\n주민등록번호 {rrn_no_hyphen} 본인 확인 완료\n",
    ]
    template = random.choice(templates)
    phone_spaced = random_phone_spaced()
    rrn_no_hyphen = random_rrn_no_hyphen()
    name = random_name()

    content = template.format(name=name, phone_spaced=phone_spaced, rrn_no_hyphen=rrn_no_hyphen)

    # 정답에는 "실제로 존재하는 PII"로 정확히 등록 (탐지 여부와 무관하게 진짜 정답은 진짜임)
    ground_truth = {"phone": [], "email": [], "rrn": [], "foreigner_id": []}
    if "{phone_spaced}" in template:
        ground_truth["phone"].append(phone_spaced)
    if "{rrn_no_hyphen}" in template:
        ground_truth["rrn"].append(rrn_no_hyphen)

    filename = f"hard_{index:03d}.txt"
    return {"filename": filename, "content": content, "ground_truth": ground_truth}


def generate_trap_file(index: int) -> dict:
    """
    PII처럼 생겼지만 실제로는 PII가 아닌 사내 코드가 들어있는 파일.
    → 오탐(FP) 유도용. 정답 라벨은 비워둠 (진짜 PII가 아니므로).
    """
    templates = [
        "발주 내역\n발주번호: {trap}\n품목: 사무용품\n수량: {n}개\n",
        "자산 관리 대장\n일련번호: {trap}\n비고: 정기 점검 완료\n",
    ]
    template = random.choice(templates)
    trap = random_trap_code()
    content = template.format(trap=trap, n=random.randint(1, 50))

    filename = f"trap_{index:03d}.txt"
    # 정답은 비어있음 — 진짜 PII가 아니기 때문
    return {"filename": filename, "content": content, "ground_truth": {"phone": [], "email": [], "rrn": [], "foreigner_id": []}}


def generate_normal_file(index: int) -> dict:
    """PII가 전혀 없는 평범한 더미 파일."""
    templates = [
        "회의록\n일시: 2026년 7월 {day}일\n참석자 수: {n}명\n안건: 서비스 개선 논의\n",
        "사내 공지\n다음 주 정기 점검이 예정되어 있습니다. 담당 부서: 운영팀\n",
        "재고 현황\n품목 코드: {code}\n수량: {n}개\n",
    ]
    template = random.choice(templates)
    content = template.format(
        day=random.randint(1, 28),
        n=random.randint(1, 100),
        code=random.randint(1000, 9999),
    )
    filename = f"normal_{index:03d}.txt"
    return {"filename": filename, "content": content, "ground_truth": {"phone": [], "email": [], "rrn": [], "foreigner_id": []}}


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    all_ground_truth = {}

    # 구성: 깔끔한 PII 50개 + 까다로운 PII(미탐 유도) 20개
    #      + 함정 코드(오탐 유도) 15개 + 완전 정상 파일 15개 = 총 100개
    for i in range(50):
        file_data = generate_pii_file(i)
        filepath = OUTPUT_DIR / file_data["filename"]
        filepath.write_text(file_data["content"], encoding="utf-8")
        all_ground_truth[file_data["filename"]] = file_data["ground_truth"]

    for i in range(20):
        file_data = generate_hard_pii_file(i)
        filepath = OUTPUT_DIR / file_data["filename"]
        filepath.write_text(file_data["content"], encoding="utf-8")
        all_ground_truth[file_data["filename"]] = file_data["ground_truth"]

    for i in range(15):
        file_data = generate_trap_file(i)
        filepath = OUTPUT_DIR / file_data["filename"]
        filepath.write_text(file_data["content"], encoding="utf-8")
        all_ground_truth[file_data["filename"]] = file_data["ground_truth"]

    for i in range(15):
        file_data = generate_normal_file(i)
        filepath = OUTPUT_DIR / file_data["filename"]
        filepath.write_text(file_data["content"], encoding="utf-8")
        all_ground_truth[file_data["filename"]] = file_data["ground_truth"]

    GROUND_TRUTH_PATH.write_text(
        json.dumps(all_ground_truth, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print("더미 파일 100개 생성 완료 (깔끔한 PII 50 + 까다로운 PII 20 + 함정코드 15 + 정상 15)")
    print(f"저장 위치: {OUTPUT_DIR}")
    print(f"정답 라벨 저장 완료: {GROUND_TRUTH_PATH}")


if __name__ == "__main__":
    main()