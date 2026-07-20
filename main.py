"""
실행 진입점.

현재는 1주차 구조만 잡혀있는 상태 (scanner가 아직 구현 전이라 실행하면 에러남).
매주 여기에 그 주차 작업 결과를 이어붙여 나갈 예정.
"""


from pathlib import Path
from src.scanner import scan_folder, extract_text_from_file
from src.masker import mask_file

TEST_FILES_DIR = Path("test_files")
OUTPUT_DIR = Path("output")


def main():
    print("=== PC 엔드포인트 PII 탐지 도구 ===")
    print(f"스캔 대상 폴더: {TEST_FILES_DIR.resolve()}")

    results = scan_folder(TEST_FILES_DIR)

    for filepath_str, detections in results.items():
        filepath = Path(filepath_str)
        print(f"\n[{filepath_str}]")
        for pii_type, matches in detections.items():
            print(f"  {pii_type}: {len(matches)}건 탐지")

        # 원본 텍스트 다시 추출해서 마스킹 처리
        text = extract_text_from_file(filepath)
        output_path = mask_file(filepath, text, detections, OUTPUT_DIR)
        print(f"  → 마스킹 결과 저장: {output_path}")


if __name__ == "__main__":
    main()