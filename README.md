# Usage
This replaces generic stalker aliases with names from your Twitch chat.

It can take a minute for Twitch to update the chat member list, so run NameGraBBer late. Run it with the game closed, then start a new game to ensure characters are generated with updated names.

# Setup
Put contents in base Anomaly folder.

Download and install [Python](https://www.python.org/downloads/), then run "python -m pip install requests" in a terminal.

Authorize NameGraBBer [here](https://id.twitch.tv/oauth2/authorize?response_type=token&client_id=w70kisl5o6k8wsbrh8w41938vw9nk6&redirect_uri=http://localhost&scope=moderator%3Aread%3Achatters), then copy your access_token from the URL bar after being redirected to an invalid web page.

Run anomaly_twitch_integration.py and enter your access_token in the terminal. Right click to paste if control v doesn't work.

# Compatibility
Tested for Anomaly 1.5.1 and 1.5.2. Only the first 1,000 chat names will be found, in alphabetical order. Information on how to expand that number can be found [here](https://dev.twitch.tv/docs/api/reference/#get-chatters).
