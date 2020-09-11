from __future__ import print_function
import pickle
import os.path

import simplejson
from dbus import service
from googleapiclient import errors
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/classroom.topics','https://www.googleapis.com/auth/classroom.courses','https://www.googleapis.com/auth/classroom.rosters']

def main():
    """Shows basic usage of the Classroom API.
    Prints the names of the first 10 courses the user has access to.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token_extes.pickle'):
        with open('token_extes.pickle', 'rb') as token:
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
        with open('token_extes.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('classroom', 'v1', credentials=creds)
    cursos = ["2021INF4A Quart d'infantil grup A", "2021INF4B Quart d'infantil grup B", "2021INF4C Quart d'infantil grup C", "2021INF4D Quart d'infantil grup D", "2021INF4E Quart d'infantil grup E",
              "2021INF5A Cinquè d'infantil grup A", "2021INF5B Cinquè d'infantil grup B", "2021INF5C Cinquè d'infantil grup C", "2021INF5D Cinquè d'infantil grup D", "2021INF5E Cinquè d'infantil grup E",
              "2021INF6A Sisè d'infantil grup A", "2021INF6B Sisè d'infantil grup B", "2021INF6C Sisè d'infantil grup C", "2021INF6D Sisè d'infantil grup D", "2021INF6E Sisè d'infantil grup E",
              "2021PRI1A Primer de primària grup A", "2021PRI1B Primer de primària grup B", "2021PRI1C Primer de primària grup C", "2021PRI1D Primer de primària grup D", "2021PRI1E Primer de primària grup E",
              "2021PRI2A Segon de primària grup A", "2021PRI2B Segon de primària grup B",
              "2021PRI2C Segon de primària grup C", "2021PRI2D Segon de primària grup D",
              "2021PRI2E Segon de primària grup E",
              "2021PRI3A Tercer de primària grup A", "2021PRI3B Tercer de primària grup B",
              "2021PRI3C Tercer de primària grup C", "2021PRI3D Tercer de primària grup D",
              "2021PRI3E Tercer de primària grup E",
              "2021PRI4A Quart de primària grup A", "2021PRI4B Quart de primària grup B",
              "2021PRI4C Quart de primària grup C", "2021PRI4D Quart de primària grup D",
              "2021PRI4E Quart de primària grup E"
              ]

    topicspri = ["Valors","Religió", "Projectes de ciències naturals - ciències socials", "Plàstica",
                 "Música","Matemàtiques", "Llengua estrangera - Anglès","Llengua catalana","Llengua castellana",
                 "Educació física","Dubtes","Informació general"]
    topicsinf = ["Psicomotricitat","Matemàtiques","Lectura i escriptura", "Grafomotricitat","Art","Anglès","Dubtes","Informació general"]
    nombre = 0
    for cursactual in cursos:
        print(cursactual)
        longitudnom = len(cursactual)
        print(cursactual[10:longitudnom])

        if cursactual[4:7] == "INF":
            tutor = "neus.homar@cide.es"

        else:
            tutor = "jonathan.bangueses@cide.es"

        course = {
                 'name': cursactual,
                 'section': 'Anual',
                 'descriptionHeading': 'Benvingut a '+ cursactual[10:longitudnom],
                 'description': """Aquest serà el punt de trobada en tot allò referent a aquest curs""",
                 'ownerId': tutor,
                 'courseState': 'ACTIVE'
        }
        course = service.courses().create(body=course).execute()

        teacher = {
            'userId': 'coordinacio-tic@cide.es'
        }
        teacher = service.courses().teachers().create(courseId=course.get('id'),
                                                      body=teacher).execute()



        ### Afegir alias

        alias = 'd:x_' + str(nombre)
        courseAlias = {
            'alias': alias
        }
        try:
            courseAlias = service.courses().aliases().create(
                courseId=course.get('id'),
                body=courseAlias).execute()
        except errors.HttpError:
            print('Alias Creation Failed')

        nombre = nombre + 1

        print(course.get('id'))
        print(cursactual[4:7])
        if cursactual[4:7] == "INF":
            topics = topicsinf
        else:
            topics = topicspri

        for ntopic in topics:
            topic = {
                "name": ntopic
            }
            print(ntopic)
            response = service.courses().topics().create(
                courseId=course.get('id'),
                body=topic).execute()

        # if cursactual[4:7] == "INF":
        #     #tutor = "neus.homar@cide.es"
        #     tutor = "xavier.sastre@cide.es"
        # else:
        #     #tutor = "jonathan.bangueses@cide.es"
        #     tutor = "coordinacio-tic@cide.es"
        #
        # teacher = {
        #     'userId': tutor
        # }
        # try:
        #     teacher = service.courses().teachers().create(courseId=course.get('id'),
        #                                                   body=teacher).execute()
        #     print(u'User {0} was added as a teacher to the course with ID "{1}"'
        #           .format(teacher.get('profile').get('name').get('fullName'),
        #                   course.get('id')))
        # except errors.HttpError as e:
        #     error = simplejson.loads(e.content).get('error')
        #     if (error.get('code') == 409):
        #         print(u'User "{0}" is already a member of this course.'.format(tutor))
        #     else:
        #         raise

        print(alias + " " + "creat")



if __name__ == '__main__':
    main()
