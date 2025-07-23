import os
import json
from kaggle.api.kaggle_api_extended import KaggleApi

def autentica_kaggle():
    os.makedirs(os.path.expanduser("~/.kaggle"), exist_ok=True)
    with open(os.path.expanduser("~/.kaggle/kaggle.json"), "w") as f:
        json.dump(kaggle_token, f)
