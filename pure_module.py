import json
import requests
import pickle
import logging
from logging.handlers import TimedRotatingFileHandler
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


###########################
#Setting the Logger details
###########################

logger = logging.getLogger(__name__)

class Pureapi(object):

    #####################################################
    # INIT FUNCTION
    #Initializing array objects
    #####################################################

    def __init__(self, hostname = "test.pure.com", api_token = "api_token", api_version="api/1.15", api_endpoint="auth/session"):

        try:
            logger.debug("Setting up a connection to {hostname}".format(hostname =  hostname))

            self.hostname = hostname
            self.api_token = api_token
            self.api_version = api_version
            self.api_endpoint = api_endpoint
            data = {"api_token" : self.api_token}
            self.params = json.dumps(data)
            self.url = "https://%s/%s/%s" %(self.hostname,  self.api_version,self.api_endpoint)
            self.session = requests.Session()
            self.session.post(self.url,self.params,headers={'Content-Type' :    'application/json'}, verify=False)
            #The below loop is to check if the session is valid and will log the status
            if (len(self.session.get("https://"+self.hostname+"/api/1.15/array?space=true").text)) < 5:
                logger.critical("Setting up a connection to {hostname} is failed".format(hostname =  self.hostname))
            else:
                logger.info("The connection to {array} was successful with session ID: {session}".format(session =  self.session, array=self.hostname))

        except:
            logger.critical("Setting up a connection to {hostname} is failed".format(hostname =  self.hostname))


    def get_array_details(self):
        """
        Returns the array details for the given array
        """
        return json.loads(self.session.get("https://"+self.hostname+"/api/1.15/array?space=true").text)

    def get_volume_details(self):
        """
        Returns the volume details for the given array
        """
        return json.loads(self.session.get("https://"+self.hostname+"/api/1.15/volume?action=monitor").text)


def query_pure_api(array, location):

    tokens = {"array1":"token1", "array2":"token2", "array":"token", "array3":"token3", "array4":"token4", "array5":"token5"}

    try:
        try:
            return (Pureapi(fqdn,api_token=   tokens[array]))
        except:
            logger.critical("API Token is not available for the array   {array}".format(array = array))

    except :

        try:
            try:
                return (Pureapi(fqdn,api_token=    tokens[array]))
            except:
                logger.critical("API Token is not available for the array   {array}".format(array = array))

        except:
            try:
                return (Pureapi(array,api_token= tokens[array]))
            except:
                logger.critical("API Token is not available for the array   {array}".format(array = array))


def generate_pure_array_object(array):
    location = array[:3]
    array_object = (query_pure_api(array,location))
    return array_object


def pure_sessions(array_list):

    session_object_dict = {}
    for array in array_list:
        session_object_dict[array] = generate_pure_array_object(array)
    return session_object_dict
