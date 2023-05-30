import argparse
import requests

hosts = ["https://tg-matrix-mirror.herokuapp.com", "http://127.0.0.1:5000"]
endpoint = "listen"

parser = argparse.ArgumentParser(description='Termux-Remote-Client')
parser.add_argument('-e', '--exec', help='Execute command on phone', required=True)
parser.add_argument('-l', '--local', help='Sends command to localhost', required=False)

args = parser.parse_args()
if args.local:
    host = hosts[1]
else:
    host = hosts[0]

def send_command():
    command = args.exec

    data = {
        "command": command
    }

    result = requests.post(f"{host}/{endpoint}", data=data)
    response = result.json()
    print(response)


send_command()