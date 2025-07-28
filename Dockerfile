FROM --platform=linux/amd64 python:3.10

WORKDIR /app

COPY process_pdfs.py .

RUN pip install pymupdf langdetect spacy && \
    python -m spacy download en_core_web_sm

CMD ["python", "process_pdfs.py"]
