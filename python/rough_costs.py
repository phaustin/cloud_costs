# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: all
#     notebook_metadata_filter: all,-language_info
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.2'
#       jupytext_version: 1.1.0
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
#   nbsphinx:
#     execute: never
#   toc:
#     base_numbering: 1
#     nav_menu: {}
#     number_sections: false
#     sideBar: true
#     skip_h1_title: true
#     title_cell: Table of Contents
#     title_sidebar: Contents
#     toc_cell: true
#     toc_position:
#       height: calc(100% - 180px)
#       left: 10px
#       top: 150px
#       width: 315.085px
#     toc_section_display: true
#     toc_window_display: true
# ---

# %% [markdown] {"toc": true}
# <h1>Table of Contents<span class="tocSkip"></span></h1>
# <div class="toc"><ul class="toc-item"><li><span><a href="#Summary" data-toc-modified-id="Summary-1">Summary</a></span></li><li><span><a href="#Example" data-toc-modified-id="Example-2">Example</a></span><ul class="toc-item"><li><span><a href="#Result" data-toc-modified-id="Result-2.1">Result</a></span></li></ul></li><li><span><a href="#Machines-needed-for-users" data-toc-modified-id="Machines-needed-for-users-3">Machines needed for users</a></span></li><li><span><a href="#Read-in-the-price-list" data-toc-modified-id="Read-in-the-price-list-4">Read in the price list</a></span></li><li><span><a href="#Input-case-parameters" data-toc-modified-id="Input-case-parameters-5">Input case parameters</a></span></li><li><span><a href="#Calculate-daily-and-total-costs" data-toc-modified-id="Calculate-daily-and-total-costs-6">Calculate daily and total costs</a></span></li><li><span><a href="#Output" data-toc-modified-id="Output-7">Output</a></span></li></ul></div>

# %% [markdown]
# # Cost calculation for Google Compute

# %% [markdown]
# ## Summary
#
# This is a plain-text version of the calculation done in this notebook:
# https://github.com/jupyterhub/zero-to-jupyterhub-k8s/blob/master/doc/ntbk
#
#
# To reproduce, first run the `write_cost_csvs.py` script:
#
# ```
# python write_cost_csvs.py
# ```
#
# which will screen-scape the google cost catalog page,
# produce two dataframes and output to csv:  `n1_machines.csv` and `disks.csv`
#
# (Note that the script depends on the requests, beautifulsoup4 and lxml modules.)
#
# This notebook reads those csv files then, given a machine type like "n1-standard-64"
# calculates the cost per student for a particular number of days/ram per student/storage per student

# %% [markdown]
# ## Example 
#
# 1000 students during a 4 month term using the cloud notebooks
# for 4 hours per day.
#
# **Parameters**
#
# ```
# num_users=1000
# ram_per_user=2.  #Gbytes
# space_per_user=3 #Gbytes
# machine_type='n1-standard-64'
# number_of_days=4*30
# hours_per_day = 4
# ```
#
# ### Result
#
# **Price per student**
#
# ```
# Disk space cost in $/student=$ 0.48
# Machine_cost in $/student=$13.13
# ```

# %% [markdown]
# ## Machines needed for users

# %%
import pandas as pd
import numpy as np

def calculate_machines_needed(users, mem_per_user, active_machine):
    """
    Parameters
    ----------
    
    users: int
       number of users
    mem_per_user: float
       ram needed per users
    active_machine: pd.Series
       machine characteristics
       
    Returns
    -------
    
    total_machines_needed: int
       number of machines needed for hosting
    """
    
    memory_per_machine = active_machine['Memory']
    total_gigs_needed = users * mem_per_user
    total_machines_needed = int(np.ceil(total_gigs_needed / memory_per_machine))
    return total_machines_needed


# %% [markdown]
# ## Read in the price list
#
# These csv files were written out by the `write_costs_csvs.py` script

# %%
n1_machines=pd.read_csv('n1_machines.csv',index_col='Machine type')
disks = pd.read_csv('disks.csv',index_col="Type")

# %%
disks

# %%
n1_machines

# %% [markdown]
# ## Input case parameters

# %%
num_users=1000
ram_per_user=2.  #Gbytes
space_per_user=3 #Gbytes
machine_type='n1-standard-64'
number_of_days=4*30
hours_per_day = 4
day_fraction = hours_per_day/24.

# %% [markdown]
# ## Calculate daily and total costs

# %%
active_machine = n1_machines.loc[machine_type]
machine_cost_daily=active_machine['Price (USD / hr)']*24. #cost per day per machine
num_machines=calculate_machines_needed(num_users,ram_per_user,active_machine)
disk_cost_daily=disks.loc['Standard provisioned space']['Price (per GB / month)']/30.  #Gbyte/day
total_storage_cost=disk_cost_daily*number_of_days*num_users*space_per_user
total_cpu_cost=machine_cost_daily*number_of_days*num_machines*day_fraction

# %% [markdown]
# ## Output

# %%
message=f"""
number of users: {num_users}
ram per user {ram_per_user} Gbytes

Machine details:
{active_machine}

Number of machines needed: {num_machines}
Disk cost {disk_cost_daily:6.4f} $/Gbytes/day

Over {number_of_days} days, total cost for {num_users} students is:

Disk space costs:  ${total_storage_cost}
cpu cost: ${total_cpu_cost}
"""
print(message)

# %%
text=f"""
Disk space cost: $/student=${total_storage_cost/num_users:5.2f}

Machine_cost: $/student=${total_cpu_cost/num_users:5.2f}
"""

print(text)

