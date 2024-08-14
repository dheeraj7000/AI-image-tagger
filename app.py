import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

st.title('Image Captioning and Tagging')

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

API_KEY = st.text_input("Enter your API Key:&nbsp;&nbsp; &nbsp;&nbsp; Get your Google Studio API key from [here](https://makersuite.google.com/app/apikey)", type="password")
if uploaded_file is not None:
    if st.button('Upload'):
        if API_KEY.strip() == '':
            st.error('Enter a valid API key')
        else:
            file_path = os.path.join("temp", uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getvalue())
            img = Image.open(file_path)
            try:
                genai.configure(api_key=API_KEY)
                model = genai.GenerativeModel('gemini-1.5-flash')
                caption = model.generate_content(["Write a caption for the image in english",img])
                tags=model.generate_content(["Generate 5 hash tags for the image in a line in english",img])
                st.image(img, caption=f"Caption: {caption.text}")
                st.write(f"Tags: {tags.text}")
            except Exception as e:
                error_msg = str(e)
                if "API_KEY_INVALID" in error_msg:
                    st.error("Invalid API Key. Please enter a valid API Key.")
                else:
                    st.error(f"Failed to configure API due to {error_msg}")
footer="""
  <style>
    /* Link styling */
    a:link, a:visited {
        color: blue; /* Standard link color */
        text-decoration: dotted; /* Dotted underline */
    }

    a:hover, a:active {
        color: skyblue; /* Hover and active state color */
    }

    /* Footer styling */
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        height: 10%;
        background-color: #001f3f; /* Dark blue background */
        font-size: 15px;
        color: white; 
        text-align: center;
        padding: 10px 0;
        box-shadow: 0px -2px 5px rgba(0, 0, 0, 0.3); /* Adds a shadow to the footer */
    }

    /* Paragraphs within the footer */
    .footer p {
        font-size: 20px;
        color: #cce7ff; /* Light blue text color */
        margin: 0;
    }

    /* Smaller text in footer */
    .footer .p {
        font-size: 10px;
        color: #cce7ff; /* Light blue text color */
    }

    /* Hover effect for links within the footer */
    .footer a:hover {
        color: white; /* Change link color to white on hover */
        text-decoration: none; /* Remove underline on hover */
    }
</style>

"""
st.markdown(footer,unsafe_allow_html=True)
