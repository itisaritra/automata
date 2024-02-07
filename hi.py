import streamlit as st
from selenium import webdriver
import time
import pandas as pd
import pytesseract
from PIL import Image

def take_screenshot(url):
    options = webdriver.ChromeOptions()                            # Create a webdriver instance
    options.add_argument('--headless')                             # To run Chrome in headless mode
    driver = webdriver.Chrome(options=options)
    driver.get(url)                                                # Navigate to the URL
    time.sleep(7)                                                  # Wait for some time to let the webpage load completely
    screenshot_path = "screenshot.png"                             # Take a screenshot
    driver.save_screenshot(screenshot_path)
    driver.quit()                                                  # Close the webdriver
    return screenshot_path

def extract_text_from_image(image_path):
    image = Image.open(image_path)                                 # Open the image
    text = pytesseract.image_to_string(image).lower()              # Perform OCR using pytesseract
    return text

def process_data(csv_file):
    students_not_found = []
    extracted_texts = []
    data = pd.read_csv(csv_file)
    for index, row in data.iterrows():
        student_name = row['Student Name'].lower()
        webpage_url = row['Webpage URL']
        screenshot_path = take_screenshot(webpage_url)
        extracted_text = extract_text_from_image(screenshot_path)
        extracted_texts.append(extracted_text)
        if student_name not in extracted_text:
            students_not_found.append(student_name)
    return students_not_found, extracted_texts

def main():
    st.header("woh wala automation wala task")
    st.write("Developed by [Aritra Ghosh](htps://itsaritra.pages.dev/)")
    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])
    if uploaded_file is not None:
        students_not_found, extracted_texts = process_data(uploaded_file)
        st.write("Defaulters:")
        st.error(students_not_found)
        # st.write("Extracted Texts:")
        # for text in extracted_texts:
        #     st.write(text)

if __name__ == "__main__":
    main()
