import json
import requests as req


ip = req.get('https://api.ipify.org/').text
print(json.dumps({"ip": f"{ip}"}))
