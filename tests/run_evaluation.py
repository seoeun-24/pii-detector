"""
3주차 작업 파일.

generated 더미 데이터를 스캔하고, ground_truth.json과 비교해서
'정규식 단독' vs '정규식+LLM 검증' 두 버전의 Precision/Recall/F1을 비교한다.

실행 방법: (프로젝트 루트에서, 가상환경 활성화된 상태에서)
    python3 tests/run_evaluation.py
"""

import sys
import json
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from src.scanner import scan_folder, scan_folder_with_llm_verification
from src.evaluator import evaluate_scan_results

GENERATED_DIR = Path("test_files/generated")
GROUND_TRUTH_PATH = Path("test_files/ground_truth.json")
RESULTS_PATH = Path("output/evaluation_results.json")


def print_metrics(title: str, metrics: dict):
    print(f"\n=== {title} ===")
    for pii_type, m in metrics.items():
        print(f"[{pii_type}]")
        print(f"  TP: {m['tp']}  FP: {m['fp']}  FN: {m['fn']}")
        print(f"  Precision: {m['precision']}  Recall: {m['recall']}  F1: {m['f1']}")


def main():
    ground_truth = json.loads(GROUND_TRUTH_PATH.read_text(encoding="utf-8"))

    print("1단계: 정규식 단독 스캔 중")
    regex_only_results = scan_folder(GENERATED_DIR)
    regex_only_metrics = evaluate_scan_results(regex_only_results, ground_truth)

    print("\n2단계: 정규식 + LLM 2차 검증 스캔 중 ")
    llm_verified_results = scan_folder_with_llm_verification(GENERATED_DIR)
    llm_verified_metrics = evaluate_scan_results(llm_verified_results, ground_truth)

    print_metrics("정규식 단독", regex_only_metrics)
    print_metrics("정규식 + LLM 2차 검증", llm_verified_metrics)

    print("\n=== 비교 요약 (overall) ===")
    before = regex_only_metrics["overall"]
    after = llm_verified_metrics["overall"]
    print(f"Precision: {before['precision']} → {after['precision']}")
    print(f"Recall:    {before['recall']} → {after['recall']}")
    print(f"F1:        {before['f1']} → {after['f1']}")

    Path("output").mkdir(exist_ok=True)
    RESULTS_PATH.write_text(
        json.dumps(
            {"regex_only": regex_only_metrics, "regex_plus_llm": llm_verified_metrics},
            ensure_ascii=False, indent=2,
        ),
        encoding="utf-8",
    )
    print(f"\n결과 저장 완료: {RESULTS_PATH}")


if __name__ == "__main__":
    main()