# yourtravelsong-app


# How to run

The backend is launched using the following command:

```
python EntryPoint
```
That will start the server on port 5000.
The API is composed by `getsuggestion` accessible via GET:

```
http://127.0.0.1:5000/getsuggestion
```

or via POST:

````commandline
curl -X post http://127.0.0.1:5000/getsuggestion -d '{"artist": "Radiohead", "title":"Creep"}' -H "Content-Type: application/json"
````


# Useful links

