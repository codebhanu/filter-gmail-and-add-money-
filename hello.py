
import imaplib
import email
import re
from datetime import datetime
from decimal import Decimal
# Connect to the email server
mail = imaplib.IMAP4_SSL('imap.gmail.com')  # Replace with your email provider's IMAP server
mail.login('youremailaddress', 'passkey from app passwords')

# Initialize total amount
total_amount = Decimal(0)

# Select the inbox
mail.select('inbox')

# Search for emails received from 
result, data = mail.search(None, '(FROM "email from ")')

# Iterate through the list of email IDs
for num in data[0].split():
    # Fetch the email data
    result, raw_email = mail.fetch(num, '(RFC822)')
    email_message = email.message_from_bytes(raw_email[0][1])

    # Extract date received
    date_received = email.utils.parsedate_to_datetime(email_message['date'])

    # Process email body
    if email_message.is_multipart():
        for part in email_message.walk():
            content_type = part.get_content_type()
            if content_type == "text/plain":
                plain_text_body = part.get_payload(decode=True).decode()
                # Check if the specific text exists in the plain text body
                specific_text = "has sent you somehng"
                if specific_text in plain_text_body:
                    # Extract the amounts from the plain text body
                    amount_matches = re.findall(r'\$\s*(\d{1,3}(?:,\d{3})*)(?:\.\d{2})?\s*\(CAD\)', plain_text_body)
                    if amount_matches:
                        # Print date received and amounts received
                        for amount_received in amount_matches:
                            print("Date Received:", date_received)
                            print("Amount Received:", amount_received)
                            amount = Decimal(amount_received.replace(',', ''))  # Remove commas and convert to Decimal
                            total_amount += amount  # Accumulate the total amount
                            print("Total amount:", total_amount)
                            print()  # Add an empty line for separation

# Print the total amount received from the email
print("Total amount received from SPATULA FOODS INC.:", total_amount)

# Close the connection
mail.close()
mail.logout()