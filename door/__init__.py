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

    result = r.json()
    if "distance" not in result or not isinstance(result["distance"], int):
        return "Malformed result"

    distance = result["distance"]
    if within_bounds(app.config["LOCKED_BOUNDS"], distance):
        state = LockState.Locked
    elif within_bounds(app.config["UNLOCKED_BOUNDS"], distance):
        state = LockState.Unlocked
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
        div {{ font-size: 18vw; }}
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

def within_bounds(bounds, distance):
    return distance >= bounds[0] and distance <= bounds[1]
