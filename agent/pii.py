"""BƯỚC 3a — PII gate TRƯỚC KHI vào context/store (12').

Đọc Guide.md (§3a) trước khi bắt đầu: Presidio không có tiếng Việt
sẵn (AnalyzerEngine() mặc định chỉ hỗ trợ "en"). Đường an toàn cho 2h là
regex recognizer + deny-list cho PERSON — coi spaCy/transformers NER là
stretch goal, KHÔNG bắt buộc.

Interface bắt buộc (tests/test_pii.py gọi trực tiếp 2 hàm này):

    detect(text: str) -> list[dict]
        Mỗi entity: {"type": str, "start": int, "end": int}
        `type` là một trong: "VN_CCCD", "VN_PHONE", "VN_BANK_ACCOUNT", "EMAIL"
        `start`/`end` là offset ký tự trong `text` (offset đầu bao gồm,
        offset cuối KHÔNG bao gồm — giống slice Python text[start:end]).
        Format này khớp với tests/vn_pii_testset.jsonl.

    redact(text: str) -> str
        Trả về `text` sau khi mọi entity từ detect() bị thay bằng
        "[REDACTED_<TYPE>]". Phải xử lý overlap/thứ tự đúng khi có nhiều
        entity (gợi ý: thay từ cuối văn bản về đầu để offset không bị lệch).

Gợi ý định dạng (không bắt buộc đúng regex này, miễn đạt ngưỡng trên test
set ở tests/vn_pii_testset.jsonl):
    VN_CCCD          12 chữ số liên tiếp
    VN_PHONE         0 + 9-10 chữ số, có thể có dấu cách/gạch ngang
    VN_BANK_ACCOUNT  8-16 chữ số liên tiếp, thường đi kèm "STK"/"số tài khoản"
    EMAIL            dạng chuẩn local@domain.tld

Đo bằng: pytest tests/test_pii.py -v -s   (in ra precision/recall)
"""
from __future__ import annotations


import re


_EMAIL_RE = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
_STK_PREFIX_RE = re.compile(r"(?:STK|stk|số tài khoản|So tai khoan)\s*(\d{8,16})\b", re.IGNORECASE)
_CCCD_PREFIX_RE = re.compile(r"(?:CCCD|cccd|căn cước|can cuoc)(?:\s+của[^\d:]*)?[:\s]+(\d{12})\b", re.IGNORECASE)
_GENERIC_CCCD_RE = re.compile(r"\b\d{12}\b")
_GENERIC_PHONE_RE = re.compile(r"\b0\d{9}\b")


def detect(text: str) -> list[dict]:
    entities = []

    # 1. EMAIL
    for m in _EMAIL_RE.finditer(text):
        entities.append({"type": "EMAIL", "start": m.start(), "end": m.end()})

    # 2. VN_BANK_ACCOUNT (explicit STK context or 8-16 digits after STK)
    stk_spans = set()
    for m in _STK_PREFIX_RE.finditer(text):
        digits_start, digits_end = m.start(1), m.end(1)
        stk_spans.add((digits_start, digits_end))
        entities.append({"type": "VN_BANK_ACCOUNT", "start": digits_start, "end": digits_end})

    # 3. VN_CCCD
    cccd_spans = set()
    for m in _CCCD_PREFIX_RE.finditer(text):
        d_start, d_end = m.start(1), m.end(1)
        if (d_start, d_end) not in stk_spans:
            cccd_spans.add((d_start, d_end))
            entities.append({"type": "VN_CCCD", "start": d_start, "end": d_end})

    for m in _GENERIC_CCCD_RE.finditer(text):
        d_start, d_end = m.start(), m.end()
        if (d_start, d_end) not in stk_spans and (d_start, d_end) not in cccd_spans:
            cccd_spans.add((d_start, d_end))
            entities.append({"type": "VN_CCCD", "start": d_start, "end": d_end})

    # 4. VN_PHONE
    phone_spans = set()
    for m in _GENERIC_PHONE_RE.finditer(text):
        p_start, p_end = m.start(), m.end()
        if (p_start, p_end) not in stk_spans and (p_start, p_end) not in cccd_spans:
            phone_spans.add((p_start, p_end))
            entities.append({"type": "VN_PHONE", "start": p_start, "end": p_end})

    entities.sort(key=lambda x: x["start"])
    return entities


def redact(text: str) -> str:
    entities = detect(text)
    sorted_entities = sorted(entities, key=lambda x: x["start"], reverse=True)
    res = text
    for e in sorted_entities:
        start, end = e["start"], e["end"]
        label = f"[REDACTED_{e['type']}]"
        res = res[:start] + label + res[end:]
    return res

