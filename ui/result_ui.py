import streamlit as st


def display_result(result):

    st.success("Verification Completed")

    st.json(result)