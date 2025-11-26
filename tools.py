from pypdf import PdfReader
from agents import function_tool
import json

USER_DATA_FILE = "user_data.json"

@function_tool
def read_user_profile():
    try:
        with open(USER_DATA_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


@function_tool
def update_user_profile(key: str, value: str):
    data = read_user_profile()
    data[key] = value
    with open(USER_DATA_FILE, "w") as f:
        json.dump(data, f)


@function_tool
def extract_text_from_pdf(file_path: str):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text
