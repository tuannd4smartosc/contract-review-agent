import streamlit as st
import PyPDF2
import docx
import openai
from ai_agents.planner import planner_agent

# Configure your OpenAI API key
openai.api_key = "your-api-key"

st.title("🧠 AI Contract Reviewer")

uploaded_file = st.file_uploader("Upload a contract", type=["pdf", "docx"])

def extract_text(file):
    if file.name.endswith(".pdf"):
        reader = PyPDF2.PdfReader(file)
        return "\n".join([page.extract_text() for page in reader.pages])
    elif file.name.endswith(".docx"):
        doc = docx.Document(file)
        return "\n".join([para.text for para in doc.paragraphs])
    return ""

def analyze_contract(text):
    prompt = (
        "You are an AI contract reviewer. Carefully read the following contract text and provide a detailed analysis. "
        "Your response should include:\n"
        "1. A summary of the contract.\n"
        "2. Identification of any ambiguous or unclear terms.\n"
        "3. Potential risks or liabilities for the parties involved.\n"
        "4. Suggestions for improving the contract to make it more robust and fair.\n\n"
        f"Contract Text:\n\n{text[:3000]}"
    )
    result = planner_agent.run(prompt)
    return result

if uploaded_file:
    contract_text = extract_text(uploaded_file)
    st.subheader("📄 Extracted Contract Text")
    st.text_area("Text Preview", contract_text[:3000], height=200)

    if st.button("🔍 Analyze Contract"):
        with st.spinner("Analyzing..."):
            analysis = analyze_contract(contract_text)
        st.subheader("🧾 AI Analysis")
        st.markdown(analysis)