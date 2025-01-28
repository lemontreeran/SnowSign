import streamlit as st
import requests
import base64

st.title("DocuSign Integration") 

# Function to send document to DocuSign for signature
def send_to_docusign(file_content, recipient_email, recipient_name):
    docusign_api_key = st.secrets["docusign_api_key"]
    account_id = st.secrets["docusign_account_id"]
    docusign_base_url = "https://demo.docusign.net/restapi"

    headers = {
        "Authorization": f"Bearer {docusign_api_key}",
        "Content-Type": "application/json"
    }

    envelope_definition = {
        "emailSubject": "Please sign this document",
        "documents": [
            {
                "documentId": "1",
                "name": "document.pdf",
                "fileExtension": "pdf",
                "documentBase64": base64.b64encode(file_content).decode()
            }
        ],
        "recipients": {
            "signers": [
                {
                    "email": recipient_email,
                    "name": recipient_name,
                    "recipientId": "1",
                    "tabs": {
                        "signHereTabs": [
                            {
                                "documentId": "1",
                                "pageNumber": "1",
                                "xPosition": "100",
                                "yPosition": "100"
                            }
                        ]
                    }
                }
            ]
        },
        "status": "sent"
    }

    response = requests.post(f"{docusign_base_url}/v2.1/accounts/{account_id}/envelopes", headers=headers, json=envelope_definition)
    return response.json()

file = st.file_uploader("Upload a document for signature", type=["pdf"])

recipient_email = st.text_input("Recipient Email")
recipient_name = st.text_input("Recipient Name")

if st.button("Send to DocuSign"):
    if file and recipient_email and recipient_name:
        file_content = file.read()
        response = send_to_docusign(file_content, recipient_email, recipient_name)
        st.sidebar.write("DocuSign Response:", response)
    else:
        st.sidebar.error("Please provide all required information.")