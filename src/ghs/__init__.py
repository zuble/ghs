# import os

import pyrootutils

ROOT_PATH = pyrootutils.setup_root(
    search_from=__file__,
    indicator=["pixi.lock"],
    pythonpath=True,
    dotenv=True,
)

# HOME_PATH = os.getenv("PATH_MNT", "~/")
