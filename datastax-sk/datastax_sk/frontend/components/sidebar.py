import streamlit as st

def sidebar(title, subheader, text, button, default):
    st.sidebar.title(title)
    st.sidebar.subheader(subheader)
    st.sidebar.text(text)
    if st.sidebar.button(button):
        return True
    else:
        return False
     




