"""
Entry point.
"copy" (default): Creates a masked copy and preserves the original.
"overwrite": Masks the original file in place (updated based on mentor feedback).
"""

from pathlib import Path
from src.scanner import scan_folder, extract_text_from_file
from src.masker import mask_file

TEST_FILES_DIR = Path("test_files")
OUTPUT_DIR = Path("output")
MASK_MODE = "copy"  # "copy" 또는 "overwrite" 중 선택


def main():
    print("=== PC 엔드포인트 PII 탐지 도구 ===")
    print(f"스캔 대상 폴더: {TEST_FILES_DIR.resolve()}")
    print(f"마스킹 모드: {MASK_MODE}")

    results = scan_folder(TEST_FILES_DIR)

    for filepath_str, detections in results.items():
        filepath = Path(filepath_str)
        print(f"\n[{filepath_str}]")
        for pii_type, matches in detections.items():
            print(f"  {pii_type}: {len(matches)}건 탐지")

        text = extract_text_from_file(filepath)
        output_path = mask_file(filepath, text, detections, OUTPUT_DIR, mode=MASK_MODE)

        if MASK_MODE == "overwrite":
            print(f"  → 원본 파일 직접 마스킹 완료: {output_path}")
        else:
            print(f"  → 마스킹 결과 저장: {output_path}")


if __name__ == "__main__":
    main()
