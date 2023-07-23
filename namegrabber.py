import requests


class NameGraBBer:
    def __init__(self, client_id, access_token):
        self.client_id = client_id
        self.access_token = access_token
        self.names = []

    def get_user_id_from_access_token(self):
        headers = {
            "Authorization": "Bearer " + str(self.access_token),
            "Client-Id": str(self.client_id),  # this is the registered api app id
        }

        try:
            response = requests.get("https://api.twitch.tv/helix/users", headers=headers)
            response.raise_for_status()
        except requests.exceptions.RequestException as error:
            print("Twitch API request error occured while attempting to access users: ")
            raise SystemExit(error)

        data = response.json()

        return data["data"][0]["id"]

    def get_chat_names_from_user_id(self, user_id, pagination_cursor = ""):
        headers = {
            "Authorization": "Bearer " + str(self.access_token),
            "Client-Id": str(self.client_id),
        }

        params = {
            "broadcaster_id": str(user_id),  # user is the streamer
            "moderator_id": str(user_id),
            "first": 1000,
            "after": str(pagination_cursor),
        }

        try:
            response = requests.get("https://api.twitch.tv/helix/chat/chatters", params=params, headers=headers)
            response.raise_for_status()
        except requests.exceptions.RequestException as error:
            print("Twitch API request error occured while attempting to access chatters: ")
            raise SystemExit(error)

        data = response.json()

        if data["pagination"]:
            print("Page limit reached, sending new request...")
            pagination_cursor = data["pagination"]["cursor"]
            self.get_chat_names_from_user_id(user_id, pagination_cursor)

        for entry in data["data"]:
            self.names.append(entry["user_name"])

        return self.names
