from typing import Optional
from api import Api


class Cosa:
    __username = None
    __password = None
    __api = None

    def __init__(self, username: str, password: str):
        self.__username = username
        self.__password = password
        self.__api = Api(self.__username, self.__password)

    __homeId = None

    def getHomeId(self) -> Optional[str]:
        if self.__homeId != None:
            return self.__homeId

        endpoints = self.__api.getEndpoints()
        if endpoints == None:
            return None

        if endpoints.__len__() == 0:
            return None

        __homeId = endpoints[0]["id"]
        return __homeId

    def setTemperature(self, targetTemp: int) -> bool:
        homeId = self.getHomeId()
        if homeId == None:
            return False

        currentStatus = self.__api.getEndpoint(homeId)
        if currentStatus == None:
            return False

        homeTemp = currentStatus["homeTemperature"]
        awayTemp = currentStatus["awayTemperature"]
        sleepTemp = currentStatus["sleepTemperature"]
        customTemp = currentStatus["customTemperature"]

        currentMode = currentStatus["mode"]
        currentOption = currentStatus["option"]

        if (
            currentMode == "manual"
            and currentOption == "custom"
            and customTemp == targetTemp
        ):
            # already set to targetTemp
            return True

        targetSetSuccess = self.__api.setTargetTemperatures(
            homeId, homeTemp, awayTemp, sleepTemp, targetTemp
        )
        if not targetSetSuccess:
            return False

        if currentMode == "manual" and currentOption == "custom":
            # already set to manual mode
            return True

        modeSetSuccess = self.__api.enableCustomMode(homeId)
        if not modeSetSuccess:
            # try revert back to previous temperature. If this fails, then it's a lost cause
            self.__api.setTargetTemperatures(
                homeId, homeTemp, awayTemp, sleepTemp, customTemp
            )
            return False

        return True

    def turnOff(self) -> bool:
        homeId = self.getHomeId()
        if homeId == None:
            return False

        currentStatus = self.__api.getEndpoint(homeId)
        if currentStatus == None:
            return False

        currentMode = currentStatus["mode"]
        currentOption = currentStatus["option"]

        if currentMode == "manual" and currentOption == "frozen":
            # already turned off
            return True

        return self.__api.disable(homeId)

    def enableSchedule(self) -> bool:
        homeId = self.getHomeId()
        if homeId == None:
            return False

        currentStatus = self.__api.getEndpoint(homeId)
        if currentStatus == None:
            return False

        currentMode = currentStatus["mode"]

        if currentMode == "schedule":
            # already enabled
            return True

        return self.__api.enableSchedule(homeId)
