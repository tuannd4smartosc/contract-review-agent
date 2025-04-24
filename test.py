import fitz  # PyMuPDF

def highlight_matches(pdf_path, output_path, search_term):
    doc = fitz.open(pdf_path)

    for page in doc:
        text_instances = page.search_for(search_term)
        for inst in text_instances:
            # Highlight the found text
            highlight = page.add_highlight_annot(inst)
            highlight.update()

    doc.save(output_path, garbage=4, deflate=True)
    doc.close()
    print(f"Highlights saved to {output_path}")

# Example usage
highlight_matches("documents/contracts/attachment_9_nondisclosure_agr_rfp-coa-2019-01-rp-a9-nda.pdf", "highlighted_output.pdf", "NONDISCLOSURE AGREEMENT")
