import json
from pathlib import Path
import shutil

file_path = Path("data/Passport/Q&A/passport_qa_full.json")
backup_path = Path("data/Passport/Q&A/passport_qa_full_backup.json")

DEFAULT_SOURCE = "https://www.epassport.gov.bd/"

topic_keywords = {
    "application_steps": ["আবেদন", "ধাপ", "apply", "application"],
    "required_documents": ["কাগজ", "ডকুমেন্ট", "প্রয়োজনীয়", "প্রয়োজনীয়", "document"],
    "fees": ["ফি", "টাকা", "খরচ", "ভ্যাট", "fee"],
    "payment": ["পেমেন্ট", "ব্যাংক", "চালান", "payment"],
    "appointment": ["অ্যাপয়েন্টমেন্ট", "appointment", "সাক্ষাৎ"],
    "biometric": ["বায়োমেট্রিক", "ফিঙ্গার", "ছবি", "biometric"],
    "delivery_time": ["ডেলিভারি", "কত দিন", "সময়", "সময়"],
    "status_check": ["স্ট্যাটাস", "status", "চেক"],
    "correction": ["সংশোধন", "ভুল", "correction"],
    "renewal": ["রিনিউ", "নবায়ন", "renewal"],
    "lost_passport": ["হারিয়ে", "হারিয়ে", "lost"],
    "foreign_mission": ["বিদেশ", "দূতাবাস", "mission"],
}

type_keywords = {
    "procedure": ["কীভাবে", "কিভাবে", "ধাপ", "প্রক্রিয়া", "প্রক্রিয়া", "process"],
    "documents": ["কাগজ", "ডকুমেন্ট", "document"],
    "fee": ["ফি", "টাকা", "খরচ", "fee"],
    "time": ["কত দিন", "সময়", "সময়", "delivery"],
    "eligibility": ["কারা", "যোগ্য", "eligibility"],
    "problem": ["সমস্যা", "ভুল", "হচ্ছে না", "problem"],
}

def detect_label(text, mapping, default):
    text = text.lower()
    for label, keywords in mapping.items():
        for keyword in keywords:
            if keyword.lower() in text:
                return label
    return default

# backup current file first
shutil.copy(file_path, backup_path)

with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

new_data = []

for i, item in enumerate(data, start=1):
    question = item.get("instruction", "")

    new_item = {
        "id": item.get("id", f"passport_{i:03d}"),
        "domain": item.get("domain", "passport"),
        "topic": item.get("topic", detect_label(question, topic_keywords, "general")),
        "question_type": item.get("question_type", detect_label(question, type_keywords, "general")),
        "instruction": item.get("instruction", ""),
        "input": item.get("input", ""),
        "output": item.get("output", ""),
        "source_url": item.get("source_url", DEFAULT_SOURCE),
        "split": item.get("split", "unsplit")
    }

    new_data.append(new_item)

with open(file_path, "w", encoding="utf-8") as f:
    json.dump(new_data, f, ensure_ascii=False, indent=2)

print(f"Done. Updated {len(new_data)} items in {file_path}")
print(f"Backup saved at {backup_path}")