import streamlit as st
import time

@st.fragment(run_every=5)
def display_current_count():
    st.write("Current count is: ", st.session_state.count)
    st.write(st.session_state.count ** 2)

@st.fragment(run_every=0.5)
def increase_counter():
    st.session_state.count += 1

if __name__ == '__main__':
    if 'count' not in st.session_state:
        st.session_state.count = 0
    display_current_count()
    increase_counter()