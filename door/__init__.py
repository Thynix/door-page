from flask import Flask
import enum
import requests

app = Flask(__name__)

app.config.from_object('config')

class LockState(enum.Enum):
    Locked = 1
    Unlocked = 2
    Unknown = 3

@app.route('/')
def door_state():
    r = requests.get(app.config["QUERY_URL"])
    if r.status_code != 200:
        return "Error code {:d}".format(r.status_code)

    # TODO: Fix invalid JSON - must be double quotes for key.
    #print(r.text)

    #result = r.json()
    #if "distance" not in result or not isinstance(result["distance"], int):
    #    return "Malformed result"

    #distance = result["distance"]
    assert r.text.startswith("{'distance': ")
    assert r.text.endswith("}")
    distance = int(r.text[len("{'distance': "):-1])
    if distance <= app.config["LOWER_THRESHOLD"] and distance > 0:
        state = LockState.Locked if app.config["LOWER_LOCKED"] else LockState.Unlocked
    elif distance >= app.config["HIGHER_THRESHOLD"]:
        state = LockState.Locked if app.config["HIGHER_LOCKED"] else LockState.Unlocked
    else:
        # 0 may indicate sensor miswiring, such as disconnected trigger pin, so
        # consider 0 to be unknown.
        state = LockState.Unknown

    content = {
        LockState.Locked:   """<div id="locked">\U0001F512 Locked</div>""",
        LockState.Unlocked: """<div id="unlocked">\U0001F513 Unlocked</div>""",
        LockState.Unknown:  """<div id="unknown">\u203D Unknown</div>""",
    }[state]
    return """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>Door Page</title>
    <style>
        body {{ background-color: slategray; }}
        div {{ font-size: 3em; }}
        #locked {{ color: green; }}
        #unlocked {{ color: red; }}
        #unknown  {{ color: yellow; }}
    </style>
  </head>
  <body>
    {}
  </body>
</html>
""".format(content)
