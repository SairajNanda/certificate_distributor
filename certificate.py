import streamlit as st
import pandas as pd
import yagmail
import os
import tempfile
import shutil

st.set_page_config(page_title="Certificate Sender", layout="centered")

st.title("📧 Certificate Sender App")
st.markdown("Send personalized certificates to students via email!")

# 1. Inputs
email_sender = st.text_input("Your Gmail address", placeholder="you@example.com")
email_password = st.text_input("App Password", type="password", help="Use a Gmail App Password (not your real one)")

uploaded_csv = st.file_uploader("Upload Student CSV (with columns: Names, Email)", type=["csv"])
cert_folder = st.text_input("Path to Certificate Folder", help="Each file should be named like: Name_Certificate.pdf")

if st.button("Send Certificates"):
    if not email_sender or not email_password or not uploaded_csv or not cert_folder:
        st.error("Please fill in all fields.")
    elif not os.path.isdir(cert_folder):
        st.error("Certificate folder path is invalid.")
    else:
        try:
            # Read CSV
            students = pd.read_csv(uploaded_csv)

            # Setup email
            yag = yagmail.SMTP(email_sender, email_password)

            sent_count = 0
            failed = []

            # Loop through and send
            for _, row in students.iterrows():
                name = row['Names']
                email = row['Email']
                filename = f"{name}_Certificate.pdf"
                filepath = os.path.join(cert_folder, filename)

                if os.path.exists(filepath):
                    try:
                        yag.send(
                            to=email,
                            subject="Your Certificate of Achievement",
                            contents=f"Dear {name},\n\nCongratulations on your achievement! 🎉\n\nPlease find your certificate attached.\n\nBest regards,\n[Your Organization]",
                            attachments=filepath
                        )
                        sent_count += 1
                    except Exception as e:
                        failed.append((name, email, str(e)))
                else:
                    failed.append((name, email, "Certificate file not found"))

            st.success(f"✅ Sent {sent_count} certificates successfully!")
            if failed:
                st.warning(f"⚠️ {len(failed)} failures:")
                for f in failed:
                    st.text(f"{f[0]} ({f[1]}): {f[2]}")

        except Exception as e:
            st.error(f"Unexpected error: {e}")
