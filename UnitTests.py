import time
import unittest
import http.client
import json
import requests
import ollama
class UnitTestCase(unittest.TestCase):

    def test_SingleCall(self):
        response = requests.post(headers={"Content-Type": "application/json"},
                                 json={'artist': 'Radiohead', 'title': 'Creep'},
                                 # json=serialized,
                                 url="http://127.0.0.1:5000/getsuggestion")
        #print(response.content)

        res = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone("success", res['status'])
        #print("Result",res['result'])
        self.assertIsNotNone(res['result'])
        self.assertIsNotNone(res['result']['offers'])
        self.assertIsNotNone(res['result']['sentiments'])
        dataString = json.dumps(res, indent=4)
        print(dataString)
    def test_ollama_chat(self):
        response = ollama.chat(model='llama3', messages=[
            {
                'role': 'user',
                'content': 'continue the code, put just code, no explanation: def helloWord():\n  ',
            },
        ])
        print(response)

        print(response['message']['content'])
        self.assertTrue(len(response['message']['content']) > 0)

    def test_ollama_complete(self):
        response = ollama.generate(model='llama3',
                                   prompt='continue the code, put just code, no explanation: def helloWord():\n  ')
        print(response)

        print(response['response'])
        self.assertTrue(len(response['response']) > 0)

    def test_ollama_sentiment_mistral(self):
        init = time.time()
        lyric = "I'm a creep, I'm a weirdo. What the hell am I doing here? I don't belong here."

        response = ollama.generate(model='mistral',
                                   prompt='return the sentiments you find in this lyric, just the sentiments, separated by commas:\n  {} '.format(
                                       lyric))
        print(response)

        print(response['response'])
        self.assertTrue(len(response['response']) > 0)
        end = time.time()
        print("Time to execute: ", (end - init) )

        init = time.time()
        lyric = "I'm a creep, I'm a weirdo. What the hell am I doing here? I don't belong here."

        response = ollama.generate(model='mistral',
                                   prompt='return the sentiments you find in this lyric, just the sentiments, separated by commas:\n  {} '.format(
                                       lyric))
        print(response)

        print(response['response'])
        self.assertTrue(len(response['response']) > 0)
        end = time.time()
        print("Time to execute expressed in seconds : ",(end - init) )

    def test_ollama_sentiment(self):

        lyric = "I'm a creep, I'm a weirdo. What the hell am I doing here? I don't belong here."

        response = ollama.generate(model='llama3',
                                   prompt='return the sentiments you find in this lyric, just the sentiments, separated by commas:\n  {} '.format(lyric))
        print(response)

        print(response['response'])
        self.assertTrue(len(response['response']) > 0)

        lyric2='''Driving faster in my car
Falling farther from just what we are
Smoke a cigarette and lie some more
These conversations kill
Falling faster in my car

Time to take her home,
Her dizzy head is conscience laden
Time to take a ride it leaves today
No conversation
Time to take her home her dizzy head is
Conscience laden
Time to wait too long, to wait too long
To wait too long

Too much walking shoes worn thin
Too much trippin' and my soul's worn thin
Time to catch her ride it leaves today
Her name is what it means
Too much walking shoe worn thin
Time to take her home
Her dizzy head is conscience laden
Time to take a ride it leaves today
No conversation

Time to take her home her dizzy head is
Conscience laden
Time to wait too long, to wait too long
To wait too long

Conversations kill
Conversations kill
Conversations kill

Time to take her home,
Her dizzy head is conscience laden
Time to take a ride it leaves today
No conversation
Time to take her home her dizzy head is
Conscience laden
Time to wait too long, to wait too long
To wait too long

Conversations kill
Conversations kill
Conversations kill'''

        response = ollama.generate(model='llama3',
                                   prompt='return the sentiments you find in this lyric, just the sentiments, separated by commas:\n  {} '.format(
                                       lyric2))
        print(response)

        print(response['response'])
        self.assertTrue(len(response['response']) > 0)

    def test_ListModels(self):
        for l in ollama.list()["models"]:
            print(l)


if __name__ == '__main__':
    unittest.main()
