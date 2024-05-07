import streamlit as st

def homepage():
    st.title("About Our Team")
    st.subheader("Let us introduce ourselves:")
    st.write("Chakaya is the brains behind this NLP code")
    st.write("Zofie is the whizz who primarily structured the report")
    st.write("Comfort is the genius that helped put together this app")
    st.write("Anthony is the jack-of-all trades, that helped in all sections")
    st.image('teamwork.jpg')

if __name__ == "__main__":
    homepage()
