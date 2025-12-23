from fastapi import FastAPI, UploadFile, File, HTTPException
from docling.document_converter import DocumentConverter,PdfFormatOption
from docling.datamodel.base_models import InputFormat
from docling.pipeline.vlm_pipeline import VlmPipeline
from docling.datamodel.pipeline_options import TableFormerMode,PipelineOptions
from docling.datamodel.pipeline_options_vlm_model import ApiVlmOptions
import tempfile
import os
from docling.datamodel.pipeline_options import PdfPipelineOptions

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
    #     pipeline_options = PipelineOptions()
        converter = DocumentConverter(format_options={
        InputFormat.PDF: PdfFormatOption(
        )
        
    })
        
        pipeline_options = PdfPipelineOptions()
        pipeline_options.do_ocr = True
        pipeline_options.do_table_structure = True
        # pipeline_options = PipelineOptions(
        #     table_mode=TableFormerMode.PRESERVE_STRUCTURE
        #         # or other modes like "PARSER_MODE"
        # )

        result = converter.convert(
            tmp_path,
            page_range=(page_start, page_end),
            pipeline_options=pipeline_options
        )

        markdown_output = result.document.export_to_markdown()
        

        return {
            "filename": file.filename,
            "pages": [page_start, page_end],
            "markdown": markdown_output
        }

    finally:
        os.remove(tmp_path)
