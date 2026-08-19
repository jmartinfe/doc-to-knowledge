from pathlib import Path
import pymupdf
import json

EXTRACTION_DIR = Path(__file__).resolve().parent.parent.parent / "extraction"

def _ensure_data_dir_exists():
    """
    Ensure that the data directory exists. If it does not exist, create it.
    """
    EXTRACTION_DIR.mkdir(parents=True, exist_ok=True)

def process_document(content: bytes):
    doc = pymupdf.open(stream=content, filetype="pdf")

    _ensure_data_dir_exists()
    
    spans = []
    lines = []
    blocks = []
    block_id = 0
    line_id = 0
    span_id = 0

    for page in doc:
        data = page.get_text("dict")

        for block in data["blocks"]:
            block_id += 1
            block_lines = []
            block_text = ""
            for line in block.get("lines", []):
                line_id += 1
                line_spans = []
                line_text = ""

                for span in line["spans"]:
                    span_id += 1
                    spans.append({
                        "id": span_id,
                        "page": page.number + 1,
                        "text": span["text"],
                        "font": span["font"],
                        "size": span["size"],
                        "flags": span["flags"],
                        "bbox": span["bbox"],
                    })

                    line_spans.append(len(spans) - 1)
                    line_text += span["text"]
                    block_text += span["text"]

                lines.append({
                    "id": line_id,
                    "page": page.number + 1,
                    "text": line_text,
                    "spans": line_spans,
                    "bbox": line["bbox"]
                })

                block_lines.append(len(lines)-1)
            
            blocks.append({
                "id": block_id,
                "page": page.number + 1,
                "text": block_text,
                "lines": block_lines,
                "bbox": block["bbox"]
            })

    with open("./extraction/spans.json", "w", encoding="utf-8") as fp:
            json.dump(spans, fp, ensure_ascii=False, indent=2)
    with open("./extraction/lines.json", "w", encoding="utf-8") as fp:
            json.dump(lines, fp, ensure_ascii=False, indent=2)
    with open("./extraction/blocks.json", "w", encoding="utf-8") as fp:
        json.dump(blocks, fp, ensure_ascii=False, indent=2)


    