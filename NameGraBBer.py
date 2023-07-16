# TODO: add error handling
# TODO: remove 1000 chatter limit
# TODO: test gamma

import requests
import json
import xml.etree.ElementTree as xml_element_tree

print("Authorization link:")
print("https://id.twitch.tv/oauth2/authorize?response_type=token&client_id=w70kisl5o6k8wsbrh8w41938vw9nk6&redirect_uri=http://localhost&scope=moderator%3Aread%3Achatters")
print("")
print("After being redirected to an invalid page you can retrieve your user access token from the url bar")
print("")
print("Example:")
print("http://localhost/#access_token= <USER_ACCESS_TOKEN> &scope=moderator%3Aread%3Achatters&token_type=bearer")
print("")
user_access_token = input("Input user access token: ")
print("")


def get_user_id_from_twitch_api():
    headers = {
        "Authorization": "Bearer " + user_access_token,
        "Client-Id": "w70kisl5o6k8wsbrh8w41938vw9nk6",  # this is the registered api app id
    }

    response = requests.get("https://api.twitch.tv/helix/users", headers=headers)
    #print(response.text)  # debug
    data = response.json()

    return data["data"][0]["id"]


def get_names_from_twitch_api():
    headers = {
        "Authorization": "Bearer " + str(user_access_token),
        "Client-Id": "w70kisl5o6k8wsbrh8w41938vw9nk6",
    }

    params = {
        "broadcaster_id": str(user_id),  # user is the streamer
        "moderator_id": str(user_id),
        "first": 1000,
    }

    response = requests.get("https://api.twitch.tv/helix/chat/chatters", params=params, headers=headers)

    #print(response.text)  # debug
    data = response.json()
    names = []

    for entry in data["data"]:
        names.append(entry["user_name"])

    return names


def add_twitch_names():
    tree = xml_element_tree.parse("reference_generate_snames.xml")
    root = tree.getroot()
    entry_amount = 0

    for name in names:
        # create elements
        entry_amount += 1  # this occurs here because update_name_amount needs the one-indexed number
        new_string_element = xml_element_tree.SubElement(root, "string", id="lname_stalker_" + str(entry_amount - 1))
        new_text_element = xml_element_tree.SubElement(new_string_element, "text")

        # format elements
        new_string_element.text = "\n\t"
        new_string_element.tail = "\n"
        new_text_element.text = name
        new_text_element.tail = "\n"

    tree.write("gamedata/configs/text/eng/st_generate_snames.xml")
    update_name_amount(entry_amount)

    return entry_amount


def update_name_amount(entry_amount):
    lines = []

    with open("reference_system.ltx", "r") as in_file:
        lines = in_file.readlines()
        lines[463] = (
            "last_name_cnt                            = " + str(entry_amount) + "\n"
        )

    with open("gamedata/configs/system.ltx", "w") as out_file:
        for line in lines:
            out_file.write(line)


user_id = get_user_id_from_twitch_api()
names = get_names_from_twitch_api()
names_added = add_twitch_names()

if names_added >= 1000:
    print("Current name limit exceeded. Only the first 1000 were added, in alphabetical order")
else:
    print("Names added: " + str(names_added))

print("Start a new game to populate the world with updated names")
input()
