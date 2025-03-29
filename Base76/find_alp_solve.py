import requests
b = 0
for i in range(1, 76):
    b += 76**i * i
b = [f"{b}"]
a = {"text": b}
r = requests.post("http://192.168.1.117:5000/api/encode", json = a)
alp = r.json()["answ"]
al = ""
for i in range(len(alp)-1, -1, -1):
    al += alp[i]
print(al)

