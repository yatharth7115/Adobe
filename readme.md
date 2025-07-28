# Challenge 1A: PDF Outline Extraction – Adobe Hackathon 2025

This project implements a multilingual and layout-aware PDF processor that extracts structured outlines (headings and title) from PDF documents and outputs JSON files compliant with the provided schema.

---

## 🧠 Overview

- Extracts document **title** and **headings (outline)** with level and page number.
- Supports **multilingual input**, including English, Hindi, and East Asian scripts.
- Uses layout, font, spacing, linguistic, and typographic features for heuristic-based detection.
- Outputs `.json` files matching Adobe's `output_schema.json`.

---

## 🛠️ Technologies & Libraries Used

| Tool        | Purpose                         |
|-------------|---------------------------------|
| `PyMuPDF`   | PDF text + layout extraction    |
| `spaCy`     | POS tagging for linguistic cues |
| `langdetect`| Multilingual language detection |
| `Docker`    | Containerized CPU-based runtime |

---
