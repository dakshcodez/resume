import os
import sys
import tempfile

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ["https://www.googleapis.com/auth/drive"]


def main():
    pdf_path = sys.argv[1]
    file_id = os.environ["GDRIVE_FILE_ID"]
    sa_key_json = os.environ["GDRIVE_SA_KEY"]

    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        f.write(sa_key_json)
        key_path = f.name

    creds = service_account.Credentials.from_service_account_file(key_path, scopes=SCOPES)
    service = build("drive", "v3", credentials=creds)

    media = MediaFileUpload(pdf_path, mimetype="application/pdf", resumable=True)
    service.files().update(fileId=file_id, media_body=media).execute()

    print(f"Updated Drive file {file_id} with {pdf_path}")


if __name__ == "__main__":
    main()
