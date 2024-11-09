import http.client
import json
from typing import Optional


def getResponseIfSuccess(response: http.client.HTTPResponse) -> Optional[dict]:
    if response.status != 200:
        return None

    data = json.loads(response.read())

    if "ok" in data and data["ok"] == 1:
        return data

    return None


class Api:
    __apiUri = "kiwi.cosa.com.tr"
    __username = None
    __password = None
    __authToken = None

    def __init__(self, username: str, password: str):
        self.__username = username
        self.__password = password

    def getHeaders(self):
        headers = {"Content-Type": "application/json"}

        if self.hasAuth():
            headers["authToken"] = self.__authToken

        return headers

    def getConnection(self) -> http.client.HTTPSConnection:
        return http.client.HTTPSConnection(self.__apiUri)

    # region Login

    def login(self) -> bool:
        payload = {"email": self.__username, "password": self.__password}

        data = self.__postWithoutAuth("/api/users/login", payload)

        if data != None and "authToken" in data:
            self.__authToken = data["authToken"]
            return True

        self.__authToken = None
        return False

    def hasAuth(self):
        return self.__authToken != None

    # endregion

    def getEndpoints(self) -> Optional[dict]:
        data = self.__get("/api/endpoints/getEndpoints")

        if data != None and "endpoints" in data:
            return data["endpoints"]

        return None

    def getEndpoint(self, endpointId: str) -> Optional[dict]:
        payload = {"endpoint": endpointId}

        data = self.__post("/api/endpoints/getEndpoint", payload)

        if data != None and "endpoint" in data:
            return data["endpoint"]

        return None

    def setTargetTemperatures(
        self,
        endpointId: str,
        homeTemp: int,
        awayTemp: int,
        sleepTemp: int,
        customTemp: int,
    ) -> bool:
        payload = {
            "endpoint": endpointId,
            "targetTemperatures": {
                "home": homeTemp,
                "away": awayTemp,
                "sleep": sleepTemp,
                "custom": customTemp,
            },
        }

        data = self.__post("/api/endpoints/setTargetTemperatures", payload)

        if data != None:
            return True

        return False

    def disable(self, endpointId: str) -> bool:
        payload = {"endpoint": endpointId, "mode": "manual", "option": "frozen"}

        data = self.__post("/api/endpoints/setMode", payload)

        if data != None:
            return True

        return False

    def enableSchedule(self, endpointId: str) -> bool:
        payload = {"endpoint": endpointId, "mode": "schedule"}

        data = self.__post("/api/endpoints/setMode", payload)

        if data != None:
            return True

        return False

    def enableCustomMode(self, endpointId: str) -> bool:
        payload = {"endpoint": endpointId, "mode": "manual", "option": "custom"}

        data = self.__post("/api/endpoints/setMode", payload)

        if data != None:
            return True

        return False

    # region Private Call Implementations

    def __post(
        self, endpoint: str, payload: dict, allowRetry: bool = True
    ) -> Optional[dict]:
        if not self.hasAuth() and not self.login():
            return None

        return self.__postWithoutAuth(endpoint, payload, allowRetry)

    def __postWithoutAuth(
        self, endpoint: str, payload: dict, allowRetry: bool = True
    ) -> Optional[dict]:
        payload = json.dumps(payload)
        headers = self.getHeaders()
        conn = self.getConnection()

        try:
            conn.request("POST", endpoint, payload, headers)
            res = conn.getresponse()
        except:
            if allowRetry:
                return self.__post(endpoint, payload, False)

            return None

        return getResponseIfSuccess(res)

    def __get(self, endpoint: str, allowRetry: bool = True) -> Optional[dict]:
        if not self.hasAuth() and not self.login():
            return None

        return self.__getWithoutAuth(endpoint, allowRetry)

    def __getWithoutAuth(
        self, endpoint: str, allowRetry: bool = True
    ) -> Optional[dict]:
        if not self.hasAuth() and not self.login():
            return None

        headers = self.getHeaders()
        conn = self.getConnection()

        try:
            conn.request("GET", endpoint, None, headers)
            res = conn.getresponse()
        except:
            if allowRetry:
                return self.__get(endpoint, False)

            return None

        return getResponseIfSuccess(res)


# endregion
