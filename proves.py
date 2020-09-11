from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/classroom.topics','https://www.googleapis.com/auth/classroom.courses']

def main():
    """Shows basic usage of the Classroom API.
    Prints the names of the first 10 courses the user has access to.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials_authorization_client.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('classroom', 'v1', credentials=creds)

    # course = {
    #     'name': "prova",
    #     'section': 'Anual',
    #     'descriptionHeading': 'Benvingut a ',
    #     'description': """Aquest serà el punt de trobada en tot allò referent a aquest curs""",
    #     'ownerId': 'coordinacio-tic@cide.es',
    #     'courseState': 'PROVISIONED'
    # }
    # course = service.courses().create(body=course).execute()



    #response = service.courses().topics().create("159743850481",topic).execute()
    topics = []
    page_token = None
    service2 = build('classroom', 'v1', credentials=creds)
    while True:
        response = service2.courses().topics().list(
            pageToken=page_token,
            pageSize=30,
            courseId=course.get('id')).execute()
        topics.extend(response.get('topic', []))
        page_token = response.get('nextPageToken', None)
        if not page_token:
            break
    if not topics:
        print('No topics found.')
    else:
        print('Topics:')
        for topic in topics:
            print('{0} ({1})'.format(topic['name'], topic['topicId']))

    topic = {
        "name": 'Example Topic 3'
    }

    response = service2.courses().topics().create(
        courseId=course.get('id'),
    body = topic).execute()
    print('Topic created: ', response['name'])

if __name__ == '__main__':
    main()
