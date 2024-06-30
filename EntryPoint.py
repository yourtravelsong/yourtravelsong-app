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
        print("Receiving {} request".format(request.method))
        counter.increment()
        print("Invoked: ", counter.get_value())
        artist = request.json["artist"]
        song = request.json["title"]
        print("Input post: ", artist, song)

        result = backend.get_suggestion(artist, song)

        return jsonify({"status": "success", "result": result})
    if request.method == 'GET':
        artist = request.args.get('artist')
        song = request.args.get('title')

        if artist is None:
            artist = request.json["artist"]
        if song is None:
            song = request.json["title"]

        print("Input get: ", artist, song)
        result = backend.get_suggestion(artist, song)
        return jsonify({"status": "success", "result": result})
    else:
        return jsonify({"status": "error", "message": "HTTP method not supported"})



if __name__ == '__main__':
    app.run(debug=True)