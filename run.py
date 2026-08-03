from app import app
import os
from flask_talisman import Talisman
permissions_policy = {
    'geolocation': '()',      # Not allowed to use geolocation 
    'microphone': '()',       # Not allowed to use Microphone
    'camera': '()',           # Not allowed to use camera in future i'll remove this
    'display-capture': '()',  # Screen recording block
    'payment': '()'           # Payment APIs block
    }

is_render = os.getenv("is_render")
if is_render:
    Talisman(app, content_security_policy=None,permissions_policy=permissions_policy)
    debug_mode = False

else:
    Talisman(app, content_security_policy=None,force_https=False,permissions_policy=permissions_policy)
    debug_mode = True


if __name__=="__main__":
    app.run(debug=debug_mode)