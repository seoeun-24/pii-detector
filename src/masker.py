"""
file for 2nd week (멘토 피드백 반영 — 3rd week).

scanner.py가 찾아낸 PII 위치를 기반으로, 원본 텍스트를 마스킹 처리.
기본값은 '사본 생성 모드'(안전)이며, mode="overwrite"로 지정하면 원본 파일 자체를 마스킹 처리하는 것도 가능(멘토 피드백 반영).
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
    한 파일의 detections(유형별 탐지 결과)를 바탕으로 텍스트 전체를 마스킹한다.
    뒤에서부터 치환해야 앞부분의 위치(인덱스)가 안 밀린다.
    """
    all_matches = []
    for pii_type, matches in detections.items():
        for value, start, end in matches:
            all_matches.append((start, end, value))

    all_matches.sort(key=lambda m: m[0], reverse=True)

    for start, end, value in all_matches:
        masked = mask_value(value)
        text = text[:start] + masked + text[end:]

    return text


def mask_file(filepath: Path, text: str, detections: dict, output_dir: Path, mode: str = "copy") -> Path:
    """
    마스킹된 텍스트를 저장한다.

    mode="copy" (기본값, 안전 모드):
        원본은 그대로 두고 output_dir에 마스킹된 사본을 새로 생성한다.
        실무에서 아직 검증 안 된 자동화 도구를 처음 도입할 때 권장하는 방식.

    mode="overwrite" (원본 직접 마스킹 모드):
        원본 파일 자체를 마스킹된 내용으로 덮어쓴다.
        PC에 남은 개인정보를 실질적으로 제거해야 하는 상황(예: PC 반납,
        정기 점검 후 즉시 조치)에 적합하지만, 되돌릴 수 없으므로 신중히 사용해야 한다.
    """
    masked_text = mask_text(text, detections)

    if mode == "overwrite":
        filepath.write_text(masked_text, encoding="utf-8")
        return filepath

    elif mode == "copy":
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / f"masked_{filepath.name}.txt"
        output_path.write_text(masked_text, encoding="utf-8")
        return output_path

    else:
        raise ValueError(f"지원하지 않는 mode 입니다: {mode} (copy 또는 overwrite만 가능)")
