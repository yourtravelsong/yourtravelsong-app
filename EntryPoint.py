from flask import Flask, jsonify,request
from Counter import Counter
from Backend import TravelBackend as Backend
app = Flask(__name__)

counter = Counter()
backend = Backend()

with app.app_context():
    print("App context init")
   # if 'singleton' not in g:
    #    g.singleton = Singleton()


@app.route('/getsuggestion', methods=['GET', 'POST'])
def get_suggestion():
    if request.method == 'POST':
        counter.increment()
        print("Invoked: ", counter.get_value())
        artist = request.json["artist"]
        song = request.json["title"]
        print("Input: ", artist, song)

        result = backend.get_suggestion(artist, song)

        return jsonify({"status": "success", "result": result})

    elif request.method == 'GET':
        return jsonify({"status": "error", "message": "GET method not supported"})
    else:
        return jsonify({"status": "error", "message": "HTTP method not supported"})



if __name__ == '__main__':
    app.run(debug=True)