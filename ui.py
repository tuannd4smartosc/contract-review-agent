import streamlit as st
from pathlib import Path
from utils.files import check_extension
from utils.extractors import extract_text_from_docx, extract_text_from_pdf

# Display the selected PDF
def display_contract_content(file_path):
    is_pdf = check_extension(file_path, ".pdf")
    is_docx = check_extension(file_path, ".docx")
    plain_text = ""
    if is_pdf:
        plain_text = extract_text_from_pdf(file_path)
    elif is_docx:
        plain_text = extract_text_from_docx(file_path)
    st.text_area("PDF Content", plain_text, height=500)

# Main Streamlit app function
def main():
    st.title("PDF Contract Viewer")

    # List of PDF files (you can modify the path as needed)
    pdf_folder = Path("documents/contracts")  # Make sure you have a folder named 'contracts' with PDFs
    pdf_files = [f.name for f in pdf_folder.glob("*.pdf")]

    if not pdf_files:
        st.error("No PDF files found in the 'contracts' folder.")
        return

    # Dropdown to select a PDF file
    selected_file = st.selectbox("Select a PDF Contract", pdf_files)

    # If a file is selected, display its content
    if selected_file:
        file_path = pdf_folder / selected_file
        display_contract_content(file_path)

if __name__ == "__main__":
    main()
