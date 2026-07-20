"""
2week file.

scanner.py가 찾아낸 PII 위치를 기반으로, 원본 텍스트를 마스킹 처리.
원본 파일은 절대 덮어쓰지 않고, output/ 폴더에 마스킹된 사본을 새로 만든다.
"""


from pathlib import Path


def mask_value(value: str) -> str:
    """
    탐지된 값 하나를 마스킹 형태로 변환.
    앞 3자리 + 가운데 마스킹 + 뒤 4자리만 보존.
    예: "010-1234-5678" -> "010-****-5678"
    """
    if len(value) <= 7:
        return value[0] + "*" * (len(value) - 1)
    return value[:3] + "*" * (len(value) - 7) + value[-4:]


def mask_text(text: str, detections: dict) -> str:
    """
    한 파일의 detections based 바탕으로 텍스트 전체를 마스킹.
    뒤에서부터 치환해야 앞부분의 위치(인덱스)가 안 밀림.
    """
    all_matches = []
    for pii_type, matches in detections.items():
        for value, start, end in matches:
            all_matches.append((start, end, value))

    # 끝 위치가 뒤에 있는 것부터 처리 (역순 정렬)
    all_matches.sort(key=lambda m: m[0], reverse=True)

    for start, end, value in all_matches:
        masked = mask_value(value)
        text = text[:start] + masked + text[end:]

    return text


def mask_file(filepath: Path, text: str, detections: dict, output_dir: Path) -> Path:
    """
    마스킹된 텍스트를 output_dir에 사본으로 저장하고, 생성된 경로를 반환.
    원본 파일은 건드리지 않게.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    masked_text = mask_text(text, detections)

    output_path = output_dir / f"masked_{filepath.name}.txt"
    output_path.write_text(masked_text, encoding="utf-8")
    return output_path
