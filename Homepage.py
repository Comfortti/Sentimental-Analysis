import streamlit as st

def homepage():
    st.title("Sentiment Analysis in Music")
    st.write("Welcome to our page on Sentiment Analysis (SA).")
    st.write("SA is a method of determining whether certain words or phrases are positive or negative, and what better way to utilise this Natural Language Processing tool than with the very subjective opinions of music albums!")
    st.write("Use the left sidebar to navigate around where you can view the sentiment of a multitude of albums in the 'Music Reviews' section or you can test out your own comments in the 'Be Sentimental' section.")
    st.image('emojieggs.jpg')
    
if __name__ == "__main__":
    homepage()