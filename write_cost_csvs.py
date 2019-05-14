"""
adapted from  https://github.com/jupyterhub/zero-to-jupyterhub-k8s/blob/master/doc/ntbk/z2jh/cost.py
Screen scapes https://cloud.google.com/compute/pricing and returns data frames with
standard machine costs (n1_machines) and storage costs (disks)
"""
import numpy as np
import pandas as pd

from google_costs import disk_df
from google_costs import machine_df

disk_df.to_csv("disks.csv", index=False)
machine_df["Machine type"] = [item.strip() for item in machine_df["Machine type"]]
machine_df["Memory"] = [item.replace("GB", "") for item in machine_df["Memory"]]
machine_df["Memory"] = [float(item) for item in machine_df["Memory"]]
machine_df.set_index("Machine type", drop=False, inplace=True)
n1_list = [item for item in machine_df.index if item.find("n1-standard") > -1]
n1_machines = machine_df.loc[n1_list]
n1_machines.to_csv("n1_machines.csv")
