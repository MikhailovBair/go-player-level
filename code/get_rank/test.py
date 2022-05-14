import requests

resp = requests.post("https://getgoprediction-kkbft5v6xa-lm.a.run.app/", files={"file": open("foo.sgf", 'rb')})
# resp = requests.post("http://localhost:5000", files={"file": open("bar.sgf", 'rb')})

print(resp.json())