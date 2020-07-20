__author__ = 'mauricio'

import logging
import requests
from fhir_config import *

BASE_URL="https://gateway.api.pcftest.com:9004"
GET_TOKEN="/v1/oauth2/token?grant_type=client_credentials"
LOGIN="/v1/oauth2/authorize/login"
LOGOUT="/v1/oauth2/authorize/logout"
PATIENT='/v1/fhir_rest/'
OBSERVATION='/v1/fhir_rest/Observation?subject._id='

logging.basicConfig(format='%(asctime)s [%(levelname)s] [%(name)s] %(message)s', level=logging.INFO)
logging.getLogger("requests").setLevel(logging.WARN)

class Philips_FHIR(object):

    def __init__(self):
        self.log = logging.getLogger("Philips_FHIR")
        self.get_auth_string()
        self.metadata = {}

    def get_auth_string(self):
        string = '%s:%s' % (KEY,SECRET)
        self.base64_auth = string.encode('base64')
        self.log.info("Encoded string %s" % self.base64_auth)

    def log_response(self, r):
        try:
            self.log.info("Response Status: %s" % r.status_code)
            self.log.info("Response Body: %s" % r.json())
        except Exception as e:
            self.log.error("Exception while logging request result: %s" % e)

    def get_token(self):

        url = BASE_URL + GET_TOKEN
        headers = {'Authorization': 'Basic ' + self.base64_auth}
        r = requests.post(url, headers=headers)
        self.log_response(r)
        if r.status_code == 200:
            self.token = r.json()['access_token']
            self.log.info("Token: %s" % self.token)
            return True
        else:
            self.log.error("Could not get token")
            return False

    def get_bearer_headers(self, type):
        return {'Authorization': 'Bearer ' + self.token,type:'application/json'}

    def login(self, credentials):
        self.records = []
        url = BASE_URL + LOGIN
        headers = self.get_bearer_headers('Content-Type')
        self.log.info("Sending request to %s" % url)
        self.log.info("Sending headers: %s" % headers)
        self.log.info("Logging in with %s" % credentials )
        r = requests.post(url, data=credentials, headers=headers)
        self.log_response(r)

        if r.status_code == 200:
            self.fhir_patient_id = r.json()['user']['fhir_patient_id']
            self.id = r.json()['user']['id']
            self.log.info("Logged in...Patient ID: %s ID: %s" % (self.fhir_patient_id, self.id))
            return True
        else:
            self.log.error("Could not log in...")
            return False

    def logout(self):
        url = BASE_URL + LOGOUT
        headers = {'Authorization': 'Bearer ' + self.token}
        requests.delete(url, headers=headers)
        self.log.info("Logged out")

    def get_patient(self):
        url = BASE_URL + PATIENT + self.fhir_patient_id
        headers = self.get_bearer_headers('Accept')
        r = requests.get(url, headers=headers)
        self.log_response(r)
        result = r.json()
        if r.status_code == 200:
            self.metadata['name'] = result['name'][0]['text']
            self.metadata['gender'] = result['gender']['coding'][0]['display']
            self.metadata['birthDate'] = result['birthDate']
            self.metadata['zip'] = result['address'][0]['zip']
            self.metadata['maritalStatus'] = result['maritalStatus']['coding'][0]['display']
            self.metadata['active'] = result['active']
            self.log.info("Patient Metadata: %s" % self.metadata)
            return True
        else:
            self.log.error("Could not get patient data...")
            return False

    def get_observation(self, next=True):

        url = BASE_URL + OBSERVATION + self.id

        if next:
            url = self.next_api_call
            if url == 'none':
                return False

        headers = self.get_bearer_headers('Accept')
        r = requests.get(url, headers=headers)
        self.log_response(r)
        result = r.json()

        if r.status_code == 200:
            self.records.extend( result['entry'] )
            self.links = result['link']
            self.next_api_call = self.get_next_url()
            self.log.info("Next API call: %s " % self.next_api_call)
            return True
        else:
            self.log.error("Could not get observation")
            return False

    def get_next_url(self):
        for link in self.links:
            if link['rel'] == 'next':
                return link['href']
        return 'none'

    def finish(self,status):
        self.logout()
        exit(status)