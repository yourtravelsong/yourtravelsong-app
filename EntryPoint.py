import logging
import os
from venv import logger
from dotenv import load_dotenv
from flask import Flask, jsonify,request
from Counter import Counter
from Backend import TravelBackend as Backend
app = Flask(__name__)

with app.app_context():
    logger.info("App context init")

@app.route('/getsuggestion', methods=['GET', 'POST'])
def get_suggestion():

    if request.method == 'GET':
        artist = request.args.get('artist')
        song = request.args.get('title')

        if artist is None:
            artist = request.json["artist"]
        if song is None:
            song = request.json["title"]

        logger.info("Input get: ", artist, song)
        result = backend.get_suggestion(artist, song)
        return jsonify({"status": "success", "result": result})

    if request.method == 'POST':
        ### TODO: this method, we could use it for retrieve the song lyric as input instead of the artist and song
        print("Receiving {} request".format(request.method))
        counter.increment()
        print("Invoked: ", counter.get_value())
        ## TODO:
        logger.warning("Method POST not already implemented as expected")
        artist = request.json["artist"]
        song = request.json["title"]
        print("Input post: ", artist, song)

        result = backend.get_suggestion(artist, song)

        return jsonify({"status": "success", "result": result})

    else:
        return jsonify({"status": "error", "message": "HTTP method not supported"})



if __name__ == '__main__':

    logger.debug("Loading env vars")
    load_dotenv("index.env")

    assert os.getenv("AMADEUS_API_KEY") is not None
    assert os.getenv("AMADEUS_SECRET_KEY") is not None
    assert os.getenv("MONGODB_CONNECTION_STRING") is not None
    assert os.getenv("MONGODB_CONNECTION_STRING_REMOTE") is not None
    assert os.getenv("MISTRAL_API_KEY") is not None
    assert os.getenv("PINECONE_API_KEY") is not None

    logging.basicConfig(level=logging.DEBUG)

    counter = Counter()
    backend = Backend()

    app.run(debug=True)