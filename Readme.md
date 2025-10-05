
# Adobe Hackathon Part A: PDF Outline Extractor

> A multilingual, layout-aware PDF processor to extract structured outlines and titles.

[](https://www.python.org/downloads/)
[](https://opensource.org/licenses/MIT)

-----

## 🧠 Overview

This project is a solution for **Challenge 1A: PDF Outline Extraction** from the Adobe Hackathon 2025. It implements a sophisticated, multilingual PDF processor designed to intelligently extract structured outlines—specifically titles and headings with their respective levels and page numbers. The core of the project is a heuristic-based engine that analyzes visual and textual cues within a document to identify its semantic structure, outputting a clean, structured JSON file that adheres to the challenge's specified schema.

-----

## ✨ Features

  - **Structured Data Extraction:** Accurately extracts the document **title** and a hierarchical **outline of headings**.
  - **Rich Metadata:** For each heading, it identifies the **text**, **level** (e.g., H1, H2), and the corresponding **page number**.
  - **Multilingual Support:** Robustly processes documents containing various scripts, including **English**, **Hindi**, and **East Asian languages**.
  - **Layout-Aware Analysis:** Employs a heuristic engine that considers a variety of features for detection:
      - **Typographic Features:** Font size, weight (bold, etc.), and style.
      - **Layout Features:** Spacing, indentation, and positioning on the page.
      - **Linguistic Cues:** Keyword analysis and sentence structure.
  - **Schema-Compliant Output:** Generates `.json` files that are fully compliant with Adobe's provided `output_schema.json`.

-----

## 🛠️ How It Works

The processor does not rely on simple text matching but instead simulates a human-like understanding of document structure. It reads a PDF page by page, analyzing text blocks for a combination of features. Larger, centered text at the beginning of a document is likely a title. Subsequent text blocks are scored based on their font size, boldness, and spacing relative to the surrounding content. This scoring system allows the tool to differentiate between body text and various heading levels, creating a precise and hierarchical outline of the document's structure.

-----

## 🚀 Getting Started

Follow these instructions to get a copy of the project up and running on your local machine.

### Prerequisites

Make sure you have Python 3.9 or higher installed on your system.

  - [Python 3.9+](https://www.python.org/downloads/)
  - `pip` (Python package installer)

### Installation

1.  **Clone the repository:**

    ```sh
    git clone https://github.com/yatharth7115/Adobe.git
    cd Adobe
    ```

2.  **Create and activate a virtual environment (recommended):**

    ```sh
    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate

    # For Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Install the required dependencies:**

    ```sh
    pip install -r requirements.txt
    ```

-----

## Usage

To process a PDF and generate the structured JSON output, run the main script from the command line.

```sh
python process_pdf.py --input <path_to_your_pdf_file.pdf> --output <path_to_output_directory>
```

**Example:**

```sh
python process_pdf.py --input ./sample_documents/report.pdf --output ./results
```

This will create a `report.json` file inside the `results` directory.

-----

## 📄 Output Schema

The tool generates a JSON file with the following structure, as specified by the challenge requirements.

**Example `output.json`:**

```json
{
  "title": {
    "text": "The Main Title of the Document",
    "page": 0
  },
  "headings": [
    {
      "text": "Introduction",
      "level": 1,
      "page": 1
    },
    {
      "text": "Background Information",
      "level": 2,
      "page": 2
    },
    {
      "text": "Methodology",
      "level": 1,
      "page": 3
    }
  ]
}
```

-----

## 📂 Project Structure

```
Adobe/
├── InputFiles/
│   └── report.pdf
├── OutputFiles/
│   └── report.json
├── Schema/
│   └── outputschema.json
├── Dockerfile
├── Readme.md
├── process_pdfs.py
└── requirements.txt
```
-----

## 🤝 Contributing

Contributions are welcome\! If you have suggestions for improving the heuristic engine or adding new features, please feel free to fork the repository and submit a pull request.

1.  Fork the Project.
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`).
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`).
4.  Push to the Branch (`git push origin feature/AmazingFeature`).
5.  Open a Pull Request.

-----

## 📜 License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

-----

## 📧 Contact

Yatharth - [@yatharth7115](https://www.google.com/search?q=https://github.com/yatharth7115) - yatharthbank7@gmail.com

Project Link: [https://github.com/yatharth7115/Adobe](https://github.com/yatharth7115/Adobe)



