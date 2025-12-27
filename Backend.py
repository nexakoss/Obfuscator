from flask import Flask, request, send_file, jsonify
import tempfile

app = Flask(__name__)

def valid_file(name):
    return name.endswith(".lua") or name.endswith(".txt")

@app.route("/help", methods=["GET"])
def help_cmd():
    return jsonify({
        "commands": [
            "/obfuscate",
            "/help"
        ]
    })

@app.route("/obfuscate", methods=["POST"])
def obfuscate():
    if "file" not in request.files:
        return jsonify({"error": "file missing"}), 400

    file = request.files["file"]

    if not file.filename or not valid_file(file.filename):
        return jsonify({"error": "invalid file type"}), 400

    content = file.read().decode("utf-8", errors="ignore")

    try:
        template = open("obfuscator_template.lua", "r", encoding="utf-8").read()
    except:
        return jsonify({"error": "template not found"}), 500

    if "{{SOURCE}}" not in template:
        return jsonify({"error": "SOURCE placeholder missing"}), 500

    output = template.replace("{{SOURCE}}", content)

    temp = tempfile.NamedTemporaryFile(delete=False, suffix=".lua")
    temp.write(output.encode("utf-8"))
    temp.close()

    return send_file(
        temp.name,
        as_attachment=True,
        download_name="obfuscated.lua"
    )

app.run(host="0.0.0.0", port=5000)
