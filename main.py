import streamlit as st
from datetime import date
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os, json
from dotenv import load_dotenv

# =========================================
# 🔐 1. Load secrets and credentials
# =========================================
load_dotenv()

# Google credentials (stored as JSON string in Streamlit secrets)
creds_json = st.secrets["api"]["USER_ID"]
if not creds_json:
    raise ValueError("❌ Missing Google API credentials in st.secrets['api']['USER_ID'].")

creds_dict = json.loads(creds_json)
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

# Allowed users (comma-separated usernames in Streamlit secrets)
allowed_users_raw = st.secrets["api"]["JSON_ID"]
allowed_users = [u.strip() for u in allowed_users_raw.split(",") if u.strip()]

# =========================================
# 👤 2. Login Section
# =========================================
st.title("🔒 Site Job Entry Portal")

with st.form("login_form"):
    username = st.text_input("Enter Login ID")
    login_button = st.form_submit_button("Login")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = None

if login_button:
    if username in allowed_users:
        st.session_state.logged_in = True
        st.session_state.username = username
        st.success(f"✅ Welcome, {username}!")
    else:
        st.error("❌ Invalid Login ID. Access Denied.")

# =========================================
# 📋 3. Only show form if logged in
# =========================================
if st.session_state.logged_in:

    spreadsheet_id = "1Zyvs8Z8tOpUenyCsRZ_msyHrChzHfUS9bIl7qY9F18w"
    sheet = client.open_by_key(spreadsheet_id).sheet1

    st.header("📋 Site Job Entry Form")

    with st.form("site_job_form"):
        st.subheader("📝 Job Details")

        site_name = st.text_input("Site Name")
        job_number = st.text_input("Job Number")
        quantity = st.number_input("Quantity (in units)", min_value=0, step=1)
        location = st.text_input("Location")

        st.subheader("👷 Personnel")
        employee_name = st.selectbox("Select Employee Name", options=["Name 1", "Name 2"])
        site_engineer = st.selectbox("Select Site Engineer (Installation)", options=["Name 1", "Name 2"])

        st.subheader("📅 Dates")
        delivery_date = st.date_input("Delivery Date", min_value=date(2000, 1, 1), max_value=date.today())
        installation_date = st.date_input("Installation Date", min_value=date(2000, 1, 1), max_value=date.today())
        removal_date = st.date_input("Removal Date", min_value=date(2000, 1, 1), max_value=date.today())
        removal_engineer = st.selectbox("Select Site Engineer (Removal)", options=["Name 1", "Name 2"])

        submitted = st.form_submit_button("Submit")

        if submitted:
            # Save to Google Sheet
            sheet.append_row([
                st.session_state.username,  # logged-in user ID
                site_name,
                job_number,
                quantity,
                location,
                employee_name,
                site_engineer,
                delivery_date.strftime("%Y-%m-%d"),
                installation_date.strftime("%Y-%m-%d"),
                removal_date.strftime("%Y-%m-%d"),
                removal_engineer
            ])

            st.success("✅ Form Submitted Successfully! (Saved to Google Sheet)")
            st.subheader("📄 Summary")
            st.write(f"**Submitted By:** {st.session_state.username}")
            st.write(f"**Site Name:** {site_name}")
            st.write(f"**Job Number:** {job_number}")
            st.write(f"**Quantity:** {quantity} units")
            st.write(f"**Location:** {location}")
            st.write(f"**Employee Name:** {employee_name}")
            st.write(f"**Site Engineer (Installation):** {site_engineer}")
            st.write(f"**Delivery Date:** {delivery_date.strftime('%B %d, %Y')}")
            st.write(f"**Installation Date:** {installation_date.strftime('%B %d, %Y')}")
            st.write(f"**Removal Date:** {removal_date.strftime('%B %d, %Y')}")
            st.write(f"**Site Engineer (Removal):** {removal_engineer}")

else:
    st.info("👆 Please log in with a valid ID to access the form.")