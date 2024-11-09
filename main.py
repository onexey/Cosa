import os
from time import sleep
from cosa import Cosa

username = os.environ.get("COSA_USERNAME")
password = os.environ.get("COSA_PASSWORD")

api = Cosa(username, password)

print("getHomeId")
print(api.getHomeId())

sleep(5)

print("setTemperature")
print(api.setTemperature(20))

sleep(5)

print("turnOff")
print(api.turnOff())

sleep(5)

print("enableSchedule")
print(api.setTemperature(22))
print(api.enableSchedule())
