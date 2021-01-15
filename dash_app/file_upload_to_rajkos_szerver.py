import pickle
import os
import requests
import subprocess
import pandas as pd
import numpy as np

df = pd.DataFrame(np.random.randint(0, 100, size=(100, 4)), columns=list("ABCD"))

data_file_path = "random_test_v2.pkl"

df.to_pickle(data_file_path)

subprocess.call(
    [
        "scp",
        "-P",
        "2222",
        "-o", 
        "StrictHostKeyChecking=no", 
        "-o", 
        "UserKnownHostsFile=/dev/null",
        data_file_path,
        "rajk@146.110.60.20:/var/www/rajk/cikkek",
    ]
)
