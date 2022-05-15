import requests

# resp = requests.post("https://gogetblunders-kkbft5v6xa-lm.a.run.app/", files={"file": open("A.sgf", 'rb')})
resp = requests.post("http://localhost:5000", files={"file": open("../B.sgf", 'rb')})

print(resp.json())