import os
from datetime import datetime

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from config.conf import SAMPLE_SPREADSHEET_ID, SAMPLE_RANGE_NAME
from django.conf import settings


path_file = os.path.join(settings.BASE_DIR, 'config')


class GoogleSheet():
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
    SAMPLE_SPREADSHEET_ID = SAMPLE_SPREADSHEET_ID
    SAMPLE_RANGE_NAME = SAMPLE_RANGE_NAME
    path_token = os.path.join(path_file, 'token.json')
    path_credentials = os.path.join(path_file, 'credentials.json')

    _service = None

    def __init__(self):
        creds = None
        if os.path.exists(self.path_token):
            creds = Credentials.from_authorized_user_file(
                self.path_token, self.SCOPES)
        else:
            creds = self._create_token
        self._service = build('sheets', 'v4', credentials=creds)

    @property
    def _create_token(self):
        flow = InstalledAppFlow.from_client_secrets_file(
            self.path_credentials, self.SCOPES)
        creds = flow.run_local_server(port=0)

        with open(self.path_token, 'w') as token:
            token.write(creds.to_json())

        return creds

    @property
    def get_data(self):
        sheet = self._service.spreadsheets()
        result = sheet.values().get(
            spreadsheetId=self.SAMPLE_SPREADSHEET_ID,
            range=self.SAMPLE_RANGE_NAME
        ).execute()

        return result.get('values', [])


def normalize_data(num, order, price, date, usd):
    if price:
        price = int(price)
        price_rub = round(price * usd, 2)
    else:
        price, price_rub = 0, 0
        day, month, year = date.split('.')
        date = datetime(year=y, month=month, day=day)
    return num, order, price, date, price_rub
