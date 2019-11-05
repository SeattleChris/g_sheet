
import os.path      # Used by both quickstart and Common code method.
from googleapiclient.discovery import build   # Google API Common Code Walk Through AND quickstart
from httplib2 import Http                     # Google API Common Code Walk Through
from oauth2client import file, client, tools  # Google API Common Code Walk Through
# from google_auth_oauthlib.flow import Flow
# import google-api-python-client
# oauth2client import client  -> google_auth_oauthlib import flow
# client.flow_from_clientsecrets -> flow.from_client_secrets_file

# import argparse
# import time
# from apiclient import discovery

FILELIST = 'saved-worksheets.txt'
# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms'
SAMPLE_RANGE_NAME = 'Class Data!A2:E'

# SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
# Scopes can be an iterable, or a space seperated string.
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
CLIENT_SECRET = 'env/client_secret.json'


def sample_read(service, id):
    """ This was in the original quickstart sample """
    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])
    if not values:
        print('No data found.')
    else:
        print('Name, Major:')
        for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            print('%s, %s' % (row[0], row[4]))


def sheet_create(service, title):
    """ This is based on a sample snippet from the guide """
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
    # oauth2client.client.flow_from_clientsecrets -> google_auth_oauthlib.flow.from_client_secrets_file
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET, SCOPES)
        # flow = Flow.from_client_secrets_file(CLIENT_SECRET, scopes=SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('sheets', 'v4', http=creds.authorize(Http()))
    return service


def modify_sheet(service, id):
    """ Currently seeing what we need to input data """

    """
    TODO Install the Python client library for Google APIs by running
    `pip install --upgrade google-api-python-client`
    """
    from pprint import pprint

    # The A1 notation of a range to search for a logical table of data.
    # Values will be appended after the last row of the table.
    range_ = 'Sheet1!A1:B2'  # TODO: Update placeholder value.

    # How the input data should be interpreted.
    value_input_option = 'USER_ENTERED'  # 'RAW' | 'USER_ENTERED' | 'INPUT_VALUE_OPTION_UNSPECIFIED'

    # How the input data should be inserted.
    insert_data_option = 'OVERWRITE'  # 'OVERWITE' | 'INSERT_ROWS'

    value_range_body = {
        "majorDimension": "ROWS",
        "range": "Sheet1!A1:B2",
        "values": [
            ["topLeft", "topRight"],
            [3, 4]
        ]
    }
    print('======== Modify Sheet ================')
    request = service.spreadsheets().values().append(
        spreadsheetId=id,
        range=range_,
        valueInputOption=value_input_option,
        insertDataOption=insert_data_option,
        body=value_range_body
        )
    response = request.execute()
    # TODO: Change code below to process the `response` dict:
    pprint(response)


def main():
    """Shows basic usage of the Sheets API. """
    # service = get_original_creds()
    service = get_creds()
    test_string = 'We got a service!' if service else 'Creds and service did not work.'
    print(test_string)
    # Sample addition
    boring = str(input('Just load & print sample worksheet? (y/n)')).lower()
    if boring == 'y':
        id = SAMPLE_SPREADSHEET_ID
        sample_read(service, id)
        return id
    title = str(input('What title do you want for the new worksheet?')).lower()
    spreadsheet = sheet_create(service, title)
    id = spreadsheet.get('spreadsheetId')
    with open(FILELIST, 'a') as file_end:
        file_end.write(f"{title},{id}")
    modify_sheet(service, id)
    return id


if __name__ == '__main__':
    main()
