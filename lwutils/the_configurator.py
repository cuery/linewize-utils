"""
___________.__
\__    ___/|  |__   ____
  |    |   |  |  \_/ __ \
  |    |   |   Y  \  ___/
  |____|   |___|  /\___  >
                \/     \/
                     _____.__                            __
  ____  ____   _____/ ____\__| ____  __ ______________ _/  |_  ___________
_/ ___\/  _ \ /    \   __\|  |/ ___\|  |  \_  __ \__  \\   __\/  _ \_  __ \
\  \__(  <_> )   |  \  |  |  / /_/  >  |  /|  | \// __ \|  | (  <_> )  | \/
 \___  >____/|___|  /__|  |__\___  /|____/ |__|  (____  /__|  \____/|__|
     \/           \/        /_____/                   \/

"""
__author__ = "Cody Harrington"
__email__ = "cody.harrington@linewize.com"

import os


def load_configuration(app, config="configuration.cfg", default_config="configuration.cfg.default", local_config=None):
    if local_config is None:
        local_config = app.name + ".cfg"

    default_config = os.path.join(app.root_path, default_config)
    if os.path.exists(default_config):
        app.config.from_pyfile(default_config)

    if os.path.exists(os.path.join(app.root_path, config)):
        app.config.from_pyfile(os.path.join(app.root_path, config))

    if os.path.exists(os.path.join(os.path.expanduser("~"), local_config)):
        app.config.from_pyfile(os.path.join(os.path.expanduser("~"), local_config))
