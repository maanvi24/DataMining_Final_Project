import streamlit as st
from summarizer import Summarizer

def generate_summary(summary, max_length, min_length, num_sentences):
    # Use BERT extractive summarizer
    summarizer = Summarizer()
    generated_summary = summarizer(summary, max_length=max_length, min_length=min_length, num_sentences=num_sentences)

    return generated_summary

def main():
    st.title("Summary Generator")

    article = st.text_area("Enter your article here...")
    max_length = st.number_input("Max Length for Summary", min_value=1)
    min_length = st.number_input("Min Length for Summary", min_value=1)
    num_sentences = st.number_input("Number of Sentences for Summary", min_value=1)

    if st.button("Generate Summary"):
        st.write("Generating Summary...")

        # Call the generate_summary function
        generated_summary = generate_summary(article, max_length, min_length, num_sentences)

        # Display the results
        st.success("Summary Generated Successfully!")
        st.subheader("Generated Summary:")
        st.write(generated_summary)

if __name__ == "__main__":
    main()
