from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
import tempfile
import docx2txt
from pdfminer.high_level import extract_text
import openpyxl  # For Excel support

load_dotenv()  # Load environment variables from .env file
genai.configure(api_key=os.environ['GOOGLE_API_KEY'])

model = genai.GenerativeModel('gemini-pro')

st.title("Gemini Bot")

file_contents = {}

# Initialize chat history with session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Ask me anything, or upload a document to search within."}
    ]

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

def process_query(query):
    # Combine file contents for search
    all_file_contents = "\n".join(file_contents.values())
    response = model.generate_content(f"Search the following text for the information requested in the query:\n{all_file_contents}\n\n{query}")

    # Display response and store in chat history
    with st.chat_message("assistant"):
        st.markdown(response.text)
    st.session_state.messages.append(
        {"role": "user", "content": query}
    )
    st.session_state.messages.append(
        {"role": "assistant", "content": response.text}
    )

# File upload with error handling and feedback
uploaded_file = st.file_uploader("Upload a document (PDF, DOCX, DOC, XLSX)", type=["pdf", "docx", "doc", "xlsx"])
if uploaded_file is not None:
    try:
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        with open(temp_file.name, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Extract text based on file type
        if uploaded_file.name.endswith((".pdf", ".PDF")):
            file_contents[temp_file.name] = extract_text(temp_file.name)
        elif uploaded_file.name.endswith((".docx", ".doc", "docm")):
            file_contents[temp_file.name] = docx2txt.process(temp_file.name)
        elif uploaded_file.name.endswith(".xlsx"):
            workbook = openpyxl.load_workbook(temp_file.name)
            active_sheet = workbook.active
            text = ""
            for row in active_sheet.iter_rows():
                for cell in row:
                    text += cell.value + " "
            file_contents[temp_file.name] = text

        st.success("File uploaded and processed successfully!")
    except Exception as e:
        st.error(f"Error processing file: {e}")
    finally:
        # Ensure temporary file cleanup
        temp_file.close()

# Accept user query and process if files are available
query = st.chat_input("Search within uploaded files:")
if query and file_contents:
    with st.chat_message("user"):
        st.markdown(query)
    process_query(query)