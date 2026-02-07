import os
ROOT_PATH = os.path.expanduser("~/.local/share/ghs")

os.makedirs(ROOT_PATH,exist_ok=True)

# import pyrootutils
# ROOT_PATH = pyrootutils.setup_root(
#     search_from=__file__,
#     indicator=["pixi.lock"],
#     pythonpath=True,
#     dotenv=True,
# )
