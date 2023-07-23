import xml.etree.ElementTree as xml_element_tree
import namegrabber


def add_twitch_names(names):
    entry_amount = 0

    try:
        tree = xml_element_tree.parse("reference_generate_snames.xml")
        root = tree.getroot()
    except IOError as error:
        print("File reference_generate_snames.xml not found: ")
        raise SystemExit(error)

    for name in names:
        entry_amount += 1  # this occurs here because update_name_amount needs the one-indexed number
        # create elements
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

    try:
        with open("gamedata/configs/system.ltx", "r") as in_file:
            lines = in_file.readlines()
            lines[463] = ("last_name_cnt                            = " + str(entry_amount) + "\n")
    except IOError as error:
        print("File gamedata/configs/system.ltx not found: ")
        raise SystemExit(error)

    with open("gamedata/configs/system.ltx", "w") as out_file:
        for line in lines:
            out_file.write(line)


def main():
    print("Authorization link:")
    print("https://id.twitch.tv/oauth2/authorize?response_type=token&client_id=w70kisl5o6k8wsbrh8w41938vw9nk6&redirect_uri=http://localhost&scope=moderator%3Aread%3Achatters")
    print("")
    print("After being redirected to an invalid page you can retrieve your user access token from the url bar")
    print("")
    print("Example:")
    print("http://localhost/#access_token= <USER_ACCESS_TOKEN> &scope=moderator%3Aread%3Achatters&token_type=bearer")
    print("")
    access_token = input("Input user access token: ")
    print("")

    name_grabber = namegrabber.NameGraBBer("w70kisl5o6k8wsbrh8w41938vw9nk6", access_token)
    user_id = name_grabber.get_user_id_from_access_token()
    names = name_grabber.get_chat_names_from_user_id(user_id)
    names_added = add_twitch_names(names)

    print("Names added: " + str(names_added))
    print("Start a new game to populate the world with updated names")
    print("")


if __name__ == "__main__":
    main()
