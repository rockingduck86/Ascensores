import streamlit as st
from datetime import date
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Google Sheets setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

# Open Google Sheet by name
# Open Google Sheet by ID (manual method)
spreadsheet_id = "1Zyvs8Z8tOpUenyCsRZ_msyHrChzHfUS9bIl7qY9F18w"  # paste your real ID
sheet = client.open_by_key(spreadsheet_id).sheet1

# Streamlit App Title
st.title("📋 Site Job Entry Form")

# Create the form
with st.form("site_job_form"):
    st.header("📝 Job Details")

    site_name = st.text_input("Site Name")
    job_number = st.text_input("Job Number")
    quantity = st.number_input("Quantity (in units)", min_value=0, step=1)
    location = st.text_input("Location")

    st.header("👷 Personnel")
    employee_name = st.selectbox("Select Employee Name", options=["Name 1", "Name 2"])
    site_engineer = st.selectbox("Select Site Engineer (Installation)", options=["Name 1", "Name 2"])

    st.header("📅 Dates")
    delivery_date = st.date_input("Delivery Date", min_value=date(2000, 1, 1), max_value=date.today())
    installation_date = st.date_input("Installation Date", min_value=date(2000, 1, 1), max_value=date.today())
    removal_date = st.date_input("Removal Date", min_value=date(2000, 1, 1), max_value=date.today())
    removal_engineer = st.selectbox("Select Site Engineer (Removal)", options=["Name 1", "Name 2"])

    submitted = st.form_submit_button("Submit")

    if submitted:
        # Save to Google Sheet
        sheet.append_row([
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
