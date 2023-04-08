import streamlit as st
import easyocr
from PIL import Image
import numpy as np
import re
import pytesseract

# Set up the OCR reader
reader = easyocr.Reader(['en'], gpu=False)

# Define regular expressions to extract information
company_name_re = r'(?:[A-Z][a-z]+\s*){1,3}(?:LLC|Inc|Corporation|Co|Ltd)'
name_re = r'[A-Z][a-z]+\s[A-Z][a-z]+'
designation_re = r'\b([A-Z][a-z]+\s*){1,3}\b(?:Manager|Director|President|Vice President|CEO|CTO|CFO|COO|CIO|Chief|Partner|Founder|Owner|Manager|Officer|Chairman|Secretary|Treasurer)'
mobile_number_re = r'(?:\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{10})'
email_re = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
website_re = r'(?:https?://)?(?:www\.)?[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
address_re = r'([0-9]+\s)?([A-Z][a-z]+\s)+[A-Z]{2}\s\d{5}'

# Define a function to extract information from the business card image
def extract_info_from_image(image_path):
    # Read the image using OCR
    result = reader.readtext(image_path)
    text = '\n'.join([r[1] for r in result])
    print(f"text type: {type(text)}")

    # Extract information from the text
    info = extract_info(text)

    return info

# Define the functions for extracting information from the business card
def extract_info(text):
    # Extract company name
    company_name = re.search(company_name_re, text)
    if company_name:
        company_name = company_name.group()
    else:
        company_name = None

    # Extract name
    name = re.search(name_re, text)
    if name:
        name = name.group()
    else:
        name = None

    # Extract designation
    designation = re.search(designation_re, text)
    if designation:
        designation = designation.group()
    else:
        designation = None

    # Extract mobile number
    mobile_number = re.search(mobile_number_re, text)
    if mobile_number:
        mobile_number = mobile_number.group()
    else:
        mobile_number = None

    # Extract email address
    email = re.search(email_re, text)
    if email:
        email = email.group()
    else:
        email = None

    # Extract website URL
    website = re.search(website_re, text)
    if website:
        website = website.group()
    else:
        website = None

    # Extract address
    address = re.search(address_re, text)
    if address:
        address = address.group()
    else:
        address = None

    return company_name, name, designation, mobile_number, email, website, address

# Define the Streamlit app
def app():
    st.title("Business Card Reader")


    # Create a file uploader
    uploaded_file = st.file_uploader("Upload an image of a business card", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Load the uploaded image
        image = Image.open(uploaded_file)

        # Display the uploaded image
        st.subheader("Uploaded Image")
        st.image(image, caption="Uploaded Image", use_column_width=True)

        # Convert the PIL Image object to a NumPy array
        np_image = np.array(image)

        # Extract text from the image using OCR
        result = reader.readtext(np_image)
        text = '\n'.join([r[1] for r in result])

        if isinstance(text, str):
            company_name, name, designation, mobile_number, email, website, address = extract_info(text)
            # Do something with the extracted information
        else:
            st.warning(
                "The OCR engine could not recognize any text in the uploaded image. Please try again with a different image.")

        # Extract information from the text
        company_name, name, designation, mobile_number, email, website, address = extract_info(text)

        # Display the extracted information in the GUI
        st.subheader("Extracted Information")
        st.write(f"Company Name: {company_name}")
        st.write(f"Card Holder Name: {name}")
        st.write(f"Designation: {designation}")
        st.write(f"Mobile Number: {mobile_number}")
        st.write(f"Email Address: {email}")
        st.write(f"Website URL: {website}")
        st.write(f"Address: {address}")

        # Display a message if any information is missing
        if not company_name or not name or not designation or not mobile_number or not email or not website or not address:
            st.warning(
                "Some information could not be extracted from the business card. Please check the image and try again.")
