from uuid import uuid4
import pymupdf
import json


def process_document(content: bytes):
    doc = pymupdf.open(stream=content, filetype="pdf")
    jsondoc = []

    for page in doc:
        data = page.get_text("dict")
        for block in data["blocks"]:
            for line in block.get("lines", []):
                for span in line["spans"]:
                    jsondoc.append({
                        "page": page.number + 1,
                        "text": span["text"],
                        "font": span["font"],
                        "size": span["size"],
                        "flags": span["flags"],
                        "bbox": span["bbox"],
                    })
    with open("data.json", "w", encoding="utf-8") as fp:
        json.dump(jsondoc, fp, ensure_ascii=False, indent=2)