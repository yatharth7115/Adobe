import fitz  # PyMuPDF
import os
import json
import re
import spacy
from collections import Counter

nlp = spacy.load("en_core_web_sm")

from pathlib import Path

INPUT_DIR = Path("/app/input")
OUTPUT_DIR = Path("/app/output")

os.makedirs(OUTPUT_DIR, exist_ok=True)

def extract_features(text, spans, bbox, page_rect, prev_bottom, page_num):
    size = max(span["size"] for span in spans)
    flags = spans[0]["flags"] if spans else 0
    x0, y0, x1, y1 = bbox
    page_width = page_rect.width

    rel_size = size / 12.0
    is_bold = bool(flags & 2**3)
    is_italic = bool(flags & 2**0)
    is_centered = abs((x0 + x1)/2 - page_width/2) < 5
    line_width = x1 - x0
    line_ratio = line_width / page_width
    indent = x0 / page_width
    space_above = (y0 - prev_bottom) / (y1 - y0) if prev_bottom else 0
    is_all_caps = text.isupper()
    is_title_case = text.istitle()
    first_word = text.split()[0] if text.split() else ""
    first_word_caps = first_word[:1].isupper()
    ends_with_colon = text.endswith(":")
    starts_num = bool(re.match(r'^(\d+[\.\)]|[A-Z]\.)', text))
    starts_bullet = text.strip().startswith(("•","-","*"))
    word_count = len(text.split())
    char_count = len(text)
    is_first_page = (page_num == 0)

    doc = nlp(text)
    noun_count = sum(1 for tok in doc if tok.pos_ == "NOUN")
    verb_count = sum(1 for tok in doc if tok.pos_ == "VERB")
    num_count  = sum(1 for tok in doc if tok.pos_ == "NUM")

    return {
        "rel_size": rel_size,
        "is_bold": is_bold,
        "is_italic": is_italic,
        "is_centered": is_centered,
        "line_ratio": line_ratio,
        "indent": indent,
        "space_above": space_above,
        "is_all_caps": is_all_caps,
        "is_title_case": is_title_case,
        "first_word_caps": first_word_caps,
        "ends_with_colon": ends_with_colon,
        "starts_num": starts_num,
        "starts_bullet": starts_bullet,
        "word_count": word_count,
        "char_count": char_count,
        "is_first_page": is_first_page,
        "noun_count": noun_count,
        "verb_count": verb_count,
        "num_count": num_count
    }

def is_heading(feat):
    if feat["word_count"] > 15 or feat["line_ratio"] > 0.85:
        return False
    if feat["is_bold"] and feat["rel_size"] < 1.15:
        return False
    score = 0
    score += 2 if feat["rel_size"] > 1.3 else 0
    score += 1 if feat["is_bold"] else 0
    score += 1 if feat["is_centered"] else 0
    score += 1 if feat["starts_num"] else 0
    score += 1 if feat["is_all_caps"] else 0
    score += 1 if feat["ends_with_colon"] else 0
    score += 1 if feat["space_above"] > 0.5 else 0
    return score >= 3

def get_level(text):
    if re.match(r'^\d+\.\d+\.', text):
        return "H3"
    if re.match(r'^\d+\.', text) or re.match(r'^[A-Z]\.', text):
        return "H2"
    return "H1"

def extract_outline(pdf_path):
    doc = fitz.open(pdf_path)
    title = None
    outline = []

    for pnum in range(len(doc)):
        page = doc[pnum]
        data = page.get_text("dict")
        prev_bottom = 0
        for block in data["blocks"]:
            if "lines" not in block:
                continue
            for line in block["lines"]:
                spans = line["spans"]
                text = "".join(span["text"] for span in spans).strip()
                if not text:
                    continue
                bbox = line["bbox"]
                feats = extract_features(text, spans, bbox, page.rect, prev_bottom, pnum)
                prev_bottom = bbox[3]

                if is_heading(feats):
                    lvl = get_level(text)
                    if pnum == 0 and lvl == "H1" and title is None:
                        title = text
                        continue
                    outline.append({"level": lvl, "text": text, "page": pnum + 1})

    # Fallback if title not found
# Fallback if title not found
# Fallback if title not found
    if not title:
        print("\n[Fallback Debug] Scanning page 1 for title candidates...\n")
        page = doc[0]
        data = page.get_text("dict")
        best_score = None
        best_line = None
        for block in data["blocks"]:
            if "lines" not in block:
                continue
            for line in block["lines"]:
                spans = line["spans"]
                text = "".join(span["text"] for span in spans).strip()
                if not text:
                    continue

                words = text.split()
                num_words = len(words)
                if num_words < 2 or num_words > 20:
                    continue

                size = max(span["size"] for span in spans)
                bbox = line["bbox"]
                x0, x1 = bbox[0], bbox[2]
                center_offset = abs((x0 + x1) / 2 - page.rect.width / 2)

                score = size * 2 - center_offset - num_words

                print(f"→ \"{text}\" | size={size:.1f}, center_offset={center_offset:.1f}, words={num_words}, score={score:.1f}")

                if best_score is None or score > best_score:
                    best_score = score
                    best_line = text

        if best_line:
            print(f"\n✅ [Fallback] Title chosen: {best_line}\n")
            title = best_line
        else:
            print("\n⚠️  [Fallback] No suitable title found on page 1.\n")




    return {"title": title or "", "outline": outline}

# === Main batch ===
for fname in os.listdir(INPUT_DIR):
    if not fname.lower().endswith(".pdf"):
        continue
    in_path = os.path.join(INPUT_DIR, fname)
    out_path = os.path.join(OUTPUT_DIR, os.path.splitext(fname)[0] + ".json")
    print(f"Processing {fname}...")
    result = extract_outline(in_path)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print(f" → Saved: {out_path}")

print("✅ All done!")
