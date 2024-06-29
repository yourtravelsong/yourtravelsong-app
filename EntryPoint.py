from flask import Flask, jsonify

app = Flask(__name__)
#books = [{'id': 1, 'title': 'Python Essentials', 'author': 'Jane Doe'}]

@app.route('/getsuggestion', methods=['GET'])
def get_books():

    #return jsonify({'books': books})
    return jsonify({"status": "success", "message": "This is a test message"})


if __name__ == '__main__':
    app.run(debug=True)