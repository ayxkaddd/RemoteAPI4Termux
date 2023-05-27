import argparse
import requests

host = "https://<yourhosthere>"
endpoint = "listen"


def send_command():
    parser = argparse.ArgumentParser(description='Termux-Remote-Client')
    parser.add_argument('-e', '--exec', help='Execute command on phone', required=True)

    args = parser.parse_args()

    command = args.exec

    data = {
        "command": command
    }

    result = requests.post(f"{host}/{endpoint}", data=data)
    response = result.json()
    print(response)


send_command()