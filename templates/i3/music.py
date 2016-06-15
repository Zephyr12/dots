from mpd import MPDClient

client = MPDClient()
client.connect("localhost", 6600)
song = client.currentsong()
status = client.status()

state_to_icon = {
    "play": "",
    "pause": "",
    "stop": ""
}
if status["state"] != "stop":
    status_line = state_to_icon[status["state"]] + ": " + song["title"]
    status_line_long = status_line
else:
    status_line = state_to_icon[status["state"]]
    status_line_long = status_line
print(status_line_long)
print(status_line)
print("")
