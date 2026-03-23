#!/usr/bin/env python3
"""
Quick test to verify Streamlit works
"""
import streamlit as st

st.set_page_config(
    page_title="Test",
    page_icon="🧪",
    layout="wide"
)

st.title("🧪 Test App")
st.write("If you see this, Streamlit is working!")
st.success("✅ Basic Streamlit UI is functioning")

# Test sidebar
with st.sidebar:
    st.write("Sidebar works too!")
