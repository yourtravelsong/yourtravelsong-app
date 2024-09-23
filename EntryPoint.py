import logging
import os
import subprocess
from itertools import count
from venv import logger
from dotenv import load_dotenv
from flask import Flask, jsonify,request

from Counter import Counter
from Backend import TravelBackend as Backend
from config import Arguments

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

        logger.info(f"Input get: {artist} {song}" )
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

def run():
    global counter, backend

    config = Arguments()
    logging.basicConfig(level=logging.getLevelName(config.log_level))
    if os.path.exists(config.env_file):
        load_dotenv(config.env_file)
    else:
        logger.warning(f"Env file not found {config.env_file}")

    assert os.getenv("AMADEUS_API_KEY") is not None
    assert os.getenv("AMADEUS_SECRET_KEY") is not None
    assert os.getenv("MONGODB_CONNECTION_STRING") is not None
    assert os.getenv("MISTRAL_API_KEY") is not None
    assert os.getenv("PINECONE_API_KEY") is not None

    counter = Counter()
    backend = Backend()

    app.run(debug=True)

def turn_off():
    app.run()


@app.route("/restart")
def restart():
    #TODO: check if this is working
    subprocess.run("shutdown -r 0", shell=True, check=True)
    return "Restarting"

@app.route("/shutdown")
def shutdown():
    #TODO: check if this is working
    subprocess.run("shutdown -h 0", shell=True, check=True)
    return "Shutting down!"

if __name__ == '__main__':
    run()