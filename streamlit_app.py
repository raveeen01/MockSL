import streamlit as st
import random
from PIL import Image
import pytesseract
import re

words = ["apple", "banana", "grape", "orange", "watermelon", "strawberry", "blueberry"]

if "page" not in st.session_state:
    st.session_state.page = "welcome"
if "name" not in st.session_state:
    st.session_state.name = ""
if "selected_module" not in st.session_state:
    st.session_state.selected_module = None
if "target_word" not in st.session_state:
    st.session_state.target_word = None

def welcome_page():
    st.title("Welcome Learner!")
    name = st.text_input("What is your name?", "")
    if st.button("Continue"):
        st.session_state.name = name
        st.session_state.page = "selection"

def selection_page():
    st.markdown(
        f"<h1 style='text-align: center;'>Hi, {st.session_state.name}!</h1>",
        unsafe_allow_html=True
    )
    st.markdown("<div class='center-text'>Choose your desired module and mode of difficulty.</div>", unsafe_allow_html=True)

    st.markdown(
        """
        <style>
        .center-text { text-align: center; margin-top: 20px; }
        .center-button { display: flex; justify-content: center; margin-top: 20px; }
        .card { text-align: center; padding: 20px; border-radius: 10px; background-color: #FFEBCC;
                border: 2px solid #FFB74D; color: #000000; font-family: Arial, sans-serif;
                height: 240px; width: 180px; margin: 15px auto; }
        .card-title { font-size: 16px; font-weight: bold; color: #333333; margin-bottom: 10px; }
        .card-content { font-size: 13px; color: #666666; line-height: 1.4; }
        </style>
        """,
        unsafe_allow_html=True
    )

    modules = {
        "A": ("PRE-K - Kinder", "CVC Words<br>Sight Words<br>Color Words<br>Shape Words<br>Animal Names"),
        "B": ("Grade 1", "High-Frequency Words<br>Simple Nouns<br>Action Words<br>Family Vocabulary<br>Basic Adjectives"),
        "C": ("Grade 2", "Synonyms and Antonyms<br>Expanded Vocabulary<br>Words Related to Seasons<br>Descriptive Adjectives<br>Word Families"),
        "D": ("Grade 3", "Academic Vocabulary<br>Context Clues Vocabulary<br>Homophones<br>Multi-Syllable Words<br>Topic-Specific Vocabulary")
    }

    cols = st.columns(len(modules))

    for index, (key, (title, content)) in enumerate(modules.items()):
        with cols[index]:
            if st.button(title, key=key):
                st.session_state.selected_module = title
                st.session_state.page = "spelling"

            st.markdown(
                f"""
                <div class='card'>
                    <div class='card-title'>{title}</div>
                    <div class='card-content'>{content}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown("<div class='center-button'>", unsafe_allow_html=True)
    if st.button("Get Started"):
        if st.session_state.selected_module:
            st.session_state.page = "spelling"
        else:
            st.warning("Please select a module before proceeding.")
    st.markdown("</div>", unsafe_allow_html=True)

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z]', '', text)
    return text.strip()

def spelling_page():
    if st.session_state.target_word is None:
        st.session_state.target_word = random.choice(words)

    st.title("Spelling Challenge")
    st.write(f"Please spell the word: **{st.session_state.target_word}**")

    uploaded_image = st.file_uploader("Upload an image of your spelling", type=["png", "jpg", "jpeg"])

    if uploaded_image is not None:
        image = Image.open(uploaded_image)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        extracted_text = pytesseract.image_to_string(image)
        
        cleaned_extracted_text = clean_text(extracted_text)
        cleaned_target_word = clean_text(st.session_state.target_word)

        st.write("Extracted Text from Image:", extracted_text)
        st.write("Cleaned Extracted Text:", cleaned_extracted_text)

        if cleaned_extracted_text == cleaned_target_word:
            st.success("Correct! You spelled the word correctly.")
        else:
            st.error("Incorrect spelling. Please try again.")

if st.session_state.page == "welcome":
    welcome_page()
elif st.session_state.page == "selection":
    selection_page()
elif st.session_state.page == "spelling":
    spelling_page()
