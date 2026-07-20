"""
3week file.

Compares the detection tool's output with the ground truth labels in the dummy dataset to calculate
Precision/ Recall/ F1-score.
"""



def compute_metrics(predicted: list, truth: list) -> dict:
    """
    predicted: List of values detected by the PII detection tool.
    truth: List of ground truth values.
    """
    predicted_set = set(predicted)
    truth_set = set(truth)

    tp = len(predicted_set & truth_set) 
    fp = len(predicted_set - truth_set)   
    fn = len(truth_set - predicted_set)   

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
    scan_results: Output returned by scanner.scan_folder().
    ground_truth: Dictionary containing the ground truth labels loaded from ground_truth.json.

    Collects detected values and corresponding ground truth values for each PII type,
    then computes Precision, Recall, and F1-score using compute_metrics().
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
