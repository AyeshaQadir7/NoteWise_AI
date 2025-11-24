import streamlit as st
from agent import main as run_agent
import asyncio
import os

st.set_page_config(page_title="NoteWise - Study Notes AI", layout="wide")
st.title("NoteWise - AI Study Notes Summarizer & Quiz Generator")

uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])
if uploaded_file:
    st.write("Uploaded:", uploaded_file.name)
    if st.button("Generate Summary & Quiz"):
        with st.spinner("Generating summary and quiz..."):
            temp_dir = "temp"
            if not os.path.exists(temp_dir):
                os.makedirs(temp_dir)
            temp_path = os.path.join(temp_dir, uploaded_file.name)
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            result = asyncio.run(run_agent(temp_path))
            st.write(result)

            os.remove(temp_path)
