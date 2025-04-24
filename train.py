from utils.files import check_extension, get_all_file_paths_recursive
from utils.extractors import extract_text_from_docx, extract_text_from_pdf, clean_html_text
from utils.vectorize import vectorize_to_qdrant
import asyncio

def train():
    print("Hello from contract-review-agent!")
    all_file_paths = get_all_file_paths_recursive("documents")
    contract_files: list[dict] = []
    for path in all_file_paths:
        is_pdf = check_extension(path, ".pdf")
        is_docx = check_extension(path, ".docx")
        plain_text = ""
        if is_pdf:
            plain_text = extract_text_from_pdf(path)
        elif is_docx:
            plain_text = extract_text_from_docx(path)
        contract_files.append({
            "source": path,
            "text": plain_text
        })
    asyncio.run(vectorize_to_qdrant(contract_files))

train()
