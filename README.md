# PII Detector
> Regex + Gemini API Based Personal Information Detection & Masking Tool

Project during the **LG U+ 2026 Global Summer Internship**.

---

# Project Overview
This project is a Python-based prototype that automatically detects and masks Personally Identifiable Information (PII) stored in local endpoint files.
The system first detects candidate PII using regular expressions and then performs contextual verification with the Gemini API to reduce false positives. Performance is evaluated using Precision, Recall, and F1-score.
The tool supports two masking modes: creating a masked copy while preserving the original file (default), or masking the original file in place.

---

# Supported PII Types
- Phone Numbers
- Email Addresses
- Korean Resident Registration Numbers (RRN)
- Foreigner Registration Numbers

---

# Project Structure
```text
pii-detector/
├── README.md
├── requirements.txt
├── src/
│   ├── patterns.py
│   ├── scanner.py
│   ├── masker.py
│   ├── llm_verifier.py
│   └── evaluator.py
├── test_files/
├── tests/
└── main.py
```

---

# Masking Modes

The tool supports two modes, controlled by the `MASK_MODE` variable in `main.py`:

| Mode | Behavior |
|---|---|
| `copy` (default) | Preserves the original file; saves a masked copy to `output/` |
| `overwrite` | Masks the original file directly, in place |

`copy` is recommended for initial testing and validation. `overwrite` is intended for scenarios where residual PII must be actively removed from the source file (e.g., PC return before offboarding, pre-migration cleanup).

---

# Local Setup
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

# Notes
- Only dummy data is included for testing.
- No real personal information is stored in this repository.
- Gemini API keys are managed through a `.env` file, which is excluded from Git.
- `overwrite` mode modifies files irreversibly; use with caution and always test with `copy` mode first.

---

# Development Timeline
- Week 1: Regex pattern design and file scanner implementation
- Week 2: Data masking and Gemini API integration
- Week 3: Performance evaluation (Precision / Recall / F1)
- Week 4: Result analysis and presentation
