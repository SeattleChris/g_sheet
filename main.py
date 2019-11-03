
import os.path      # Used by both quickstart and Common code method.
from googleapiclient.discovery import build   # Google API Common Code Walk Through AND quickstart
from httplib2 import Http                     # Google API Common Code Walk Through
from oauth2client import file, client, tools  # Google API Common Code Walk Through

# import argparse
# import time
# from apiclient import discovery


# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms'
SAMPLE_RANGE_NAME = 'Class Data!A2:E'

# SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
# Scopes can be an iterable, or a space seperated string.
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
CLIENT_SECRET = 'env/client_secret.json'


def sample_create(service):
    """ This is a sample snippet from the guide """
    title = 'test'
    spreadsheet = {'properties': {'title': title}}
    spreadsheet = service.spreadsheets().create(body=spreadsheet,
                                                fields='spreadsheetId').execute()
    print('Spreadsheet ID: {0}'.format(spreadsheet.get('spreadsheetId')))
    return spreadsheet


def get_original_creds():
    """ Modularizing the code that gets the appropriate credentials """
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    import pickle

    creds = None
    # If modifying these scopes, delete the file token.pickle.
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('env/token.pickle'):
        with open('env/token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'env/client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('env/token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    service = build('sheets', 'v4', credentials=creds)
    return service


def get_creds():
    """ This approach based on Google API common code walkthrough """
    STORAGE = 'env/storage.json'
    if not os.path.exists(STORAGE):
        raise EnvironmentError('Missing file')
    store = file.Storage(STORAGE)
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET, SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('sheets', 'v4', http=creds.authorize(Http()))
    return service


def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    # service = get_original_creds()
    service = get_creds()
    test_string = 'We got a service!' if service else 'Creds and service did not work.'
    print(test_string)
    # Sample addition
    spreadsheet = sample_create(service)
    # id = SAMPLE_SPREADSHEET_ID
    id = spreadsheet.get('spreadsheetId')
    cells = SAMPLE_RANGE_NAME
    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=id,
                                range=cells).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        print('Name, Major:')
        for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            print('%s, %s' % (row[0], row[4]))


if __name__ == '__main__':
    main()
