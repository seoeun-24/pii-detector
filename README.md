#PII Detector

> Regex + Gemini API Based Personal Information Detection & Masking Tool

 Project during the **LG U+ 2026 Global Summer Internship**.

---

# Project Overview

This project is a Python-based prototype that automatically detects and masks Personally Identifiable Information (PII) stored in local endpoint files.

The system first detects candidate PII using regular expressions and then performs contextual verification with the Gemini API to reduce false positives. Performance is evaluated using Precision, Recall, and F1-score.

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

---

# Development Timeline

- Week 1: Regex pattern design and file scanner implementation
- Week 2: Data masking and Gemini API integration
- Week 3: Performance evaluation (Precision / Recall / F1)
- Week 4: Result analysis and presentation
