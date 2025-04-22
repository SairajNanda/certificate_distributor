import pandas as pd
import yagmail
import os

# Configuration
EMAIL_SENDER = 'nandapk68@gmail.com'
EMAIL_PASSWORD = 'hqon hewi tssv ojzu'  
CERTIFICATES_FOLDER = '/Users/mr.sairajnanda/Desktop/test/certficates'


CSV_FILE = '/Users/mr.sairajnanda/Desktop/test/students.csv' 


EMAIL_SUBJECT = "Your Certificate of Achievement"
EMAIL_BODY = """
Dear {name},

Congratulations on your achievement! 🎉

Please find your certificate attached to this email.

Best regards,  
[Your Name or Organization]
"""

yag = yagmail.SMTP(EMAIL_SENDER, EMAIL_PASSWORD)


students = pd.read_csv(CSV_FILE)

for _, row in students.iterrows():
    name = row['Names']
    email = row['Email']
    filename = f"{name}_Certificate.pdf"
    filepath = os.path.join(CERTIFICATES_FOLDER, filename)

    if os.path.exists(filepath):
        try:
            yag.send(
                to=email,
                subject=EMAIL_SUBJECT,
                contents=EMAIL_BODY.format(name=name),
                attachments=filepath
            )
            print(f"✅ Sent to {name} at {email}")
        except Exception as e:
            print(f"❌ Failed to send to {name} at {email}: {e}")
    else:
        print(f"📁 Certificate not found for {name}: {filepath}")
