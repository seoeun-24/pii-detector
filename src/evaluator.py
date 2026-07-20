"""
3주차 작업 파일.

더미 데이터셋에 미리 붙여둔 정답 라벨과, 탐지 도구의 실제 출력 결과를 비교해서
Precision / Recall / F1 스코어를 계산한다.
"""



def compute_metrics(predicted: list, truth: list) -> dict:
    """
    predicted: 탐지 도구가 찾아낸 값들의 리스트
    truth: 정답(ground truth) 값들의 리스트
    """
    predicted_set = set(predicted)
    truth_set = set(truth)

    tp = len(predicted_set & truth_set)   # 둘 다 있는 것 = 제대로 맞춘 것
    fp = len(predicted_set - truth_set)   # 우리만 찾은 것 = 오탐
    fn = len(truth_set - predicted_set)   # 정답에만 있는 것 = 놓친 것(미탐)

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) > 0 else 0.0

    return {
        "tp": tp, "fp": fp, "fn": fn,
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1": round(f1, 4),
    }


def evaluate_scan_results(scan_results: dict, ground_truth: dict) -> dict:
    """
    scan_results: scanner.scan_folder()의 반환값
    ground_truth: ground_truth.json을 로드한 dict

    PII 유형별로 탐지값/정답값을 모아서 compute_metrics를 적용한다.
    """
    pii_types = ["phone", "email", "rrn", "foreigner_id"]

    predicted_by_type = {t: [] for t in pii_types}
    truth_by_type = {t: [] for t in pii_types}

    for filename, type_dict in ground_truth.items():
        for pii_type, values in type_dict.items():
            truth_by_type[pii_type].extend(values)

    for filepath, detections in scan_results.items():
        for pii_type, matches in detections.items():
            values = [m[0] for m in matches]
            predicted_by_type[pii_type].extend(values)

    results = {}
    for pii_type in pii_types:
        results[pii_type] = compute_metrics(predicted_by_type[pii_type], truth_by_type[pii_type])

    all_predicted = [v for values in predicted_by_type.values() for v in values]
    all_truth = [v for values in truth_by_type.values() for v in values]
    results["overall"] = compute_metrics(all_predicted, all_truth)

    return results