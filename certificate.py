import streamlit as st
import pandas as pd
import yagmail
import os
import tempfile
import shutil

st.set_page_config(page_title="Certificate Sender", layout="centered")

st.title("📧 Certificate Sender App")
st.markdown("Easily send personalized certificates to students via email!")

# Email credentials
email_sender = st.text_input("Your Gmail Address", placeholder="you@gmail.com")
email_password = st.text_input("App Password", type="password", help="Use a Gmail App Password")

# File uploads
uploaded_csv = st.file_uploader("Upload Student CSV (with columns: Names, Email)", type=["csv"])
uploaded_zip = st.file_uploader("Upload Certificate ZIP File", type=["zip"])

if st.button("📤 Send Certificates"):
    if not email_sender or not email_password or not uploaded_csv or not uploaded_zip:
        st.error("Please fill in all fields and upload both files.")
    else:
        try:
            # Step 1: Create temporary directory
            with tempfile.TemporaryDirectory() as temp_dir:
                zip_path = os.path.join(temp_dir, "certs.zip")

                # Save and unzip the uploaded ZIP
                with open(zip_path, "wb") as f:
                    f.write(uploaded_zip.read())
                shutil.unpack_archive(zip_path, temp_dir)

                # Step 2: Read student data
                students = pd.read_csv(uploaded_csv)

                # Step 3: Setup email client
                yag = yagmail.SMTP(email_sender, email_password)

                sent_count = 0
                failed = []

                # Step 4: Loop through each student
                for _, row in students.iterrows():
                    name = row['Names']
                    email = row['Email']
                    filename = f"{name}_Certificate.pdf"
                    filepath = os.path.join(temp_dir, filename)

                    if os.path.exists(filepath):
                        try:
                            yag.send(
                                to=email,
                                subject="🎉 Your Clashothon Certificate is Here!",
                                contents=f"Dear {name},\n\nThank you for being a part of Clashothon – your energy, creativity, and competitive spirit made it truly unforgettable! 🎉\n\nWe’re thrilled to share your Certificate of Participation (attached to this email) as a token of appreciation for your involvement.\n Keep the spirit alive, and we hope to see you in more exciting events ahead!\n\nIf you have any queries or feedback, feel free to reach out.\nBest regards,\nTeam ClashoThon \nTESSERACT X Rampage",
                                attachments=filepath
                            )
                            sent_count += 1
                        except Exception as e:
                            failed.append((name, email, str(e)))
                    else:
                        failed.append((name, email, "Certificate not found"))

                # Step 5: Summarycd
                st.success(f"✅ Sent {sent_count} certificates successfully!")
                if failed:
                    st.warning(f"⚠️ {len(failed)} failed:")
                    for f in failed:
                        st.text(f"{f[0]} ({f[1]}): {f[2]}")

        except Exception as e:
            st.error(f"❌ Unexpected error: {e}")
# Thank you for being a part of Clashothon – your energy, creativity, and competitive spirit made it truly unforgettable!

# We’re thrilled to share your Certificate of Participation (attached to this email) as a token of appreciation for your involvement.
# Keep the spirit alive, and we hope to see you in more exciting events ahead!

# If you have any queries or feedback, feel free to reach out.

# Best regards,
# Team ClashoThon
# TESSERACT X Rampage