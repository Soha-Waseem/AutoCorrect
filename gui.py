import streamlit as st
from nlp import spell_correct_sentence
from model import grammar_correct

st.set_page_config(
    page_title="Autocorrect Pro",
    page_icon="✨",
    layout="centered"
)

st.title("Intelligent Autocorrect Tool")
#st.markdown("**Hybrid NLP + Transformer-based text correction**")

st.markdown("---")

text = st.text_area("Enter your text below:", height=150, placeholder="Type a sentence with spelling and grammar mistakes...")

col1, col2 = st.columns([1, 5])
with col1:
    correct_btn = st.button("Correct Text", type="primary")

if correct_btn:
    if text.strip() == "":
        st.warning("Please enter some text to correct.")
    else:
        with st.spinner("Running Hybrid Correction Pipeline..."):
            # Step 1: Rule-based NLP Spelling Correction
            spell_corrected = spell_correct_sentence(text)
            
            # Step 2: Transformer-based Grammar Correction
            final_output = grammar_correct(spell_corrected)

        st.markdown("---")
        st.subheader("Results")
        
        # Display results in a structured way
        st.info(f"**Original:**\n\n{text}")
        
        # Check if there were spelling changes
        if spell_corrected != text:
            st.warning(f"**Step 1 (Spell Check):**\n\n{spell_corrected}")
        else:
            st.success(f"**Step 1 (Spell Check):** No spelling errors detected.")

        # Check if there were grammar changes
        if final_output != spell_corrected:
            st.success(f"**Step 2 (Final Grammar & Context):**\n\n{final_output}")
        else:
            st.success(f"**Step 2 (Final Grammar & Context):** No grammar issues detected.")
            
        st.markdown("### ✨ Final Corrected Text")
        st.code(final_output, language="text")