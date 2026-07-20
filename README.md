# PC 엔드포인트 PII 탐지 및 마스킹 도구

LG유플러스 2026 Global Summer Internship 멘토링 PJT

## 프로젝트 개요
PC 로컬 파일(txt/csv/docx/pdf/xlsx)에 남아있는 개인식별정보(PII)를
정규표현식으로 자동 탐지하고 마스킹하는 프로토타입.
2주차부터는 LLM API 기반 2차 검증을 결합해 정규식 단독 대비
오탐 개선 효과를 정량적으로(Precision/Recall/F1) 비교한다.

## 탐지 대상 PII (4종)
1. 전화번호
2. 이메일
3. 주민등록번호
4. 외국인등록번호

## 폴더 구조
```
pii-detector/
├── README.md
├── requirements.txt
├── src/
│   ├── __init__.py
│   ├── patterns.py       # PII 유형별 정규식 패턴 (1주차)
│   ├── scanner.py        # 폴더 재귀 탐색 + 파일별 텍스트 추출 (1주차)
│   ├── masker.py         # 탐지된 PII 마스킹 처리 (2주차)
│   ├── llm_verifier.py   # LLM API 기반 2차 검증 (2주차)
│   └── evaluator.py      # Precision/Recall/F1 계산 (3주차)
├── test_files/            # 더미(가상) 테스트 데이터 — 진짜 개인정보 절대 넣지 않기
├── tests/
│   └── test_patterns.py  # 정규식 패턴 단위 테스트
├── output/                # 마스킹된 결과 파일이 저장되는 곳 (원본은 건드리지 않음)
└── main.py                # 실행 진입점
```

## 로컬 환경 세팅 (맥 기준)

터미널에서 프로젝트 폴더로 이동한 뒤:

```bash
# 1. 가상환경 생성
python3 -m venv venv

# 2. 가상환경 활성화
source venv/bin/activate

# 3. 패키지 설치
pip install -r requirements.txt

# 4. 정상 설치 확인
python3 -c "import docx, pypdf, openpyxl; print('설치 완료!')"
```

작업을 마칠 땐 `deactivate` 명령으로 가상환경을 빠져나가면 된다.
다음에 다시 작업할 땐 `source venv/bin/activate`만 다시 실행하면 됨.

## 주의사항
- `test_files/` 안에는 **가짜(더미) 데이터만** 넣는다. 실제 개인정보 절대 금지.
- 마스킹 결과는 원본을 덮어쓰지 않고 `output/`에 사본으로 저장한다.
- LLM API 키는 코드에 직접 쓰지 않고 환경변수(`.env`)로 관리한다 (2주차에 설정).

## 진행 로그
- [ ] 1주차: 정규식 패턴 설계 + 파일 스캐너 구현
- [ ] 2주차: 마스킹 로직 + 더미 데이터셋 제작 + LLM API 연동
- [ ] 3주차: 성능 측정 (Precision/Recall/F1), 정규식 단독 vs +AI 비교
- [ ] 4주차: 결과 정리 + 발표자료
