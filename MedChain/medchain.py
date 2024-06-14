from os import environ
import logging
import requests
from util import strg2hex, hex2strg

logging.basicConfig(level="INFO")
logger = logging.getLogger(__name__)

rollup_server = environ["ROLLUP_HTTP_SERVER_URL"]
logger.info(f"HTTP rollup_server url is {rollup_server}")

def add_notice(data):
    logger.info(f"Adding notice {data}")
    notice = {"payload":  strg2hex(data)}
    response = requests.post(rollup_server + "/notice", json=notice)
    logger.info(f"Received notice status {response.status_code} body {response.content}")
    
def add_report(output = ""):
    logger.info("Adding report")
    report = {"payload": strg2hex(output)}
    response = requests.post(rollup_server + "/report", json=report)
    logger.info(f"Received report status {response.status_code}")

def handle_advance(data):
    logger.info(f"Received advance request data {data}")
    return "accept"

def handle_inspect(data):
    logger.info(f"Received inspect request data {data}")
    return "accept"

handlers = {
    "advance_state": handle_advance,
    "inspect_state": handle_inspect,
}

# Functions to interact with the rollup server

# Funtion to register a patient (with their medication routine) - ADVANCE
def register_patient():
    logger.info("Registering patient")
    patient = {"name": "John Doe", "age": 30, "medicine": "aspirin", "dose": "1 pill", "frequency": "daily", "duration": "1 week", "start_date": "2022-01-01", "end_date": "2022-01-07"},
    response = requests.post(rollup_server + "/patient", json=patient)
    logger.info(f"Received patient status {response.status_code}")
    return response.json()

# Function to get patient (and medication routine) - INSPECT
def get_patient():
    logger.info("Getting patient")
    response = requests.get(rollup_server + "/patient")
    logger.info(f"Received patient status {response.status_code}")
    return response.json()

# Function to add medication given - ADVANCE
def insert_medication_given():
    logger.info("Inserting medication given")
    medication_given = {"medication": "aspirin"}
    response = requests.post(rollup_server + "/medication_given", json=medication_given)
    logger.info(f"Received medication given status {response.status_code}")
    return response.json()

# Function to compare medication given with the routine - ADVANCE
def compare_medication_routine():
    logger.info("Comparing medication routine")
    #set() == set()
    response = requests.get(rollup_server + "/medication_routine")
    logger.info(f"Received medication routine status {response.status_code}")
    return response.json()

advance_method_handlers = {
    "patient": register_patient,
    "medication_given": insert_medication_given,
    "compare_medication_routine": compare_medication_routine,
}

inspect_method_handlers = {
    "patient": get_patient,
}

finish = {"status": "accept"}

{"method": "create_challenge"}

while True:
    logger.info("Sending finish")
    response = requests.post(rollup_server + "/finish", json=finish)
    logger.info(f"Received finish status {response.status_code}")
    if response.status_code == 202:
        logger.info("No pending rollup request, trying again")
    else:
        rollup_request = response.json()
        data = rollup_request["data"]
        
        handler = handlers[rollup_request["request_type"]]
        finish["status"] = handler(rollup_request["data"])
