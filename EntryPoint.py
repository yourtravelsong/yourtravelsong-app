from flask import Flask, jsonify,request
import Backend
app = Flask(__name__)

@app.route('/getsuggestion', methods=['GET', 'POST'])
def get_booksPOST():
    if request.method == 'POST':

        artist = request.json["artist"]
        song = request.json["title"]
        print("Input: ", artist, song)

        result = Backend.get_suggestion(artist, song)

        return jsonify({"status": "success", "message": "This is a test message POST: {}".format(result), "result": result})

    elif request.method == 'GET':
        return jsonify({"status": "success", "message": "This is a test message GET"})
    else:
        return jsonify({"status": "error", "message": "HTTP method not supported"})



if __name__ == '__main__':
    app.run(debug=True)