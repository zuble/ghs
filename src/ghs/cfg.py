import os
import os.path as osp
from dataclasses import dataclass

from InquirerPy import get_style

from ghs import ROOT_PATH


@dataclass
class Config:
    GH_UNAME = "zuble"
    JSON_FILE = osp.join(ROOT_PATH, f"assets/{GH_UNAME}_stars.json")
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    HOME_PATH = os.getenv("PATH_MNT","")
    assert HOME_PATH
    # defaults at InquirerPy.prompts.fuzzy
    # kbs = {
    # 	"up": [{"key": "up"}],
    # 	"down": [{"key": "down"}],
    # 	"toggle": [],
    # 	"toggle-all": [{"key": "c-r"}],
    # 	"toggle-down": [{"key": "c-space"},], ## <<<<<<
    # 	"toggle-exact": [{"key": "c-e"}], ## <<<<<
    # 	"open-url": [{"key": "c-o"}],  ## <<<<<<<<
    # 	"toggle-all-true" : [{"key": "c-a"},], ## <<<<<<<<<
    # }

    # https://inquirerpy.readthedocs.io/en/latest/pages/style.html
    style = get_style(
        {
            "questionmark": "#e5c07b",
            "answermark": "#e5c07b",
            "answer": "#a1dd86",  # <<< match marker (selected ones)
            "marker": "#a1dd86",  # <<<<<<<<
            "input": "#e5a1ff",  # <<< match match
            # "question": "",
            # "answered_question": "",
            # "instruction": "#abb2bf",
            "choice_name": "#a4a2a2",  # <<<<< grey light
            "choice_instruction": "#696969",  # <<<<< grey dark
            # "long_instruction": "#abb2bf",
            "pointer": "#ffffff",  # <<<<<<<< white
            # "checkbox": "#98c379",
            # "separator": "",
            # "skipped": "#5c6370",
            # "validator": "",
            "fuzzy_prompt": "#e5a1ff ",  # <<< match match
            "fuzzy_info": "#abb2bf",
            "fuzzy_border": "#4b5263",
            "fuzzy_match": "#e5a1ff",  # <<<< match match
            # "spinner_pattern": "#e5c07b",
            # "spinner_text": "",
        },
        style_override=False,
    )


cfg = Config()
