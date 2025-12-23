from fastapi import FastAPI, UploadFile, File, HTTPException
from docling.document_converter import DocumentConverter
import tempfile
import os

app = FastAPI()

@app.post("/convert")
async def convert_pdf(
    file: UploadFile = File(...),
    page_start: int = 1,
    page_end: int = 1
):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    try:
        converter = DocumentConverter()
        result = converter.convert(
            tmp_path,
            page_range=(page_start, page_end)
        )

        markdown_output = result.document.export_to_doctags()

        return {
            "filename": file.filename,
            "pages": [page_start, page_end],
            "markdown": markdown_output
        }

    finally:
        os.remove(tmp_path)
