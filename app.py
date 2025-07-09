import streamlit as st
import pandas as pd
import re

# ----------------------------
# Email Validator Function
# ----------------------------
def is_valid_email(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w{2,4}$"
    return re.match(pattern, email) is not None

# ----------------------------
# Streamlit UI
# ----------------------------
st.set_page_config(page_title="Lead Cleaner Tool", layout="centered")
st.title("Lead Deduplicator & Email Verifier")
st.markdown("Upload a CSV file with columns like `Email`, `Name`, `Company`, etc.")

uploaded_file = st.file_uploader("Upload your leads file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.subheader("Raw Data Preview")
    st.dataframe(df)

    # Remove duplicates by email
    df = df.drop_duplicates(subset="Email", keep="first")

    # Check email validity
    df["Email Valid"] = df["Email"].apply(is_valid_email)

    # Filter invalid emails
    valid_leads = df[df["Email Valid"] == True]

    st.subheader("Valid & Unique Leads")
    st.dataframe(valid_leads)

    # Download button
    csv = valid_leads.to_csv(index=False).encode("utf-8")
    st.download_button("Download Cleaned Leads", data=csv, file_name="cleaned_leads.csv", mime="text/csv")

    st.success(f"Found {len(valid_leads)} valid, unique leads!")

else:
    st.info("Please upload a CSV file to get started.")
