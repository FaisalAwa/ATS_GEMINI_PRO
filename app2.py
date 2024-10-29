from dotenv import load_dotenv

load_dotenv()

import streamlit as st
import os
import io
from PIL import Image
import pdf2image
import google.generativeai as genai
import base64

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        # Convert the pdf to image
        images = pdf2image.convert_from_bytes(uploaded_file.read())
        
        first_image = images[0]  # Get the first page as an image

        # Convert to bytes
        img_byte_arr = io.BytesIO()
        first_image.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()  # encode
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No File Uploaded")

def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Custom CSS for styling
def add_custom_css():
    st.markdown(
        """
        <style>
        body {
            background-color: #001f3f;
            color: #FFFF00;
        }
        .header {
            text-align: center;
            font-size: 36px;
            font-weight: bold;
            color: #FFFF00;
        }
        .subheader {
            text-align: center;
            font-size: 20px;
            font-weight: bold;
            color: #FFFF00;
        }
        .description {
            font-size: 18px;
            color: #FFFF00;
        }
        .stTextInput > div > input {
            background-color: #001f3f;
            color: #FFFF00;
        }
        .stButton > button {
            background-color: #001f3f;
            color: #FFFF00;
        }
        .stFileUploader > label {
            background-color: #001f3f;
            color: #FFFF00;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

add_custom_css()

# Load the image and convert it to base64
base64_image = get_base64_image("ATS.png")

# Streamlit app
# st.set_page_config(page_title='ATS Resume Expert')

# SVG Animation with LLM image
st.markdown(f"""
<svg width="100%" height="200" xmlns="http://www.w3.org/2000/svg">
  <g>
    <title>LLM</title>
    <rect width="100%" height="200" fill="#001f3f" />
    <rect x="10%" y="20" width="80%" height="160" fill="#AAAAAA" />
    <image x="15%" y="30" width="70%" height="140" href="data:image/png;base64,{base64_image}" />
  </g>
</svg>
""", unsafe_allow_html=True)

st.markdown('<div class="header">ATS Tracking System 📄🤖</div>', unsafe_allow_html=True)
st.markdown('<div class="subheader">Upload your resume and get a detailed analysis!</div>', unsafe_allow_html=True)

input_text = st.text_area("Job Description: ", key="input")
upload_file = st.file_uploader("Upload your resume (PDF)....", type=["pdf"])

if upload_file is not None:
    st.write("PDF uploaded successfully")

submit1 = st.button("Tell me about the Resume")
submit3 = st.button("Percentage Match")

input_prompt1 = """
You are an experienced HR With Tech Experience in the field of any one job role from Data Science, Full stack Web Development, Big Data Engineer, DevOps, Data Analyst. Your task is to review the provided resume against the job description for these profiles.
Please share your professional evaluation on whether the candidate's profile aligns with this role.
Highlight the strengths and weaknesses of the applicant in relation to the specific job role.
"""
input_prompt3 = """
You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of any one job from Data Science, Full stack Web Development, Big Data Engineer, DevOps, Data Analyst and deep ATS functionality.
Evaluate the resume against the provided job description, give me the percentage of match if the resume matches the job description. First, the output should come as a percentage and then keywords missing and last final thoughts.
"""

if submit1:
    if upload_file is not None:
        pdf_content = input_pdf_setup(upload_file)
        response = get_gemini_response(input_text, pdf_content, input_prompt1)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload the resume")
elif submit3:
    if upload_file is not None:
        pdf_content = input_pdf_setup(upload_file)
        response = get_gemini_response(input_text, pdf_content, input_prompt3)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload the resume")
