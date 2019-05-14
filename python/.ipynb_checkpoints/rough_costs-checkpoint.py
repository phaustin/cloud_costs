# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: all
#     notebook_metadata_filter: all,-language_info
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.2'
#       jupytext_version: 1.1.1
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
#   toc:
#     base_numbering: 1
#     nav_menu: {}
#     number_sections: true
#     sideBar: true
#     skip_h1_title: false
#     title_cell: Table of Contents
#     title_sidebar: Contents
#     toc_cell: true
#     toc_position: {}
#     toc_section_display: true
#     toc_window_display: true
# ---

# %% [markdown] {"toc": true}
# <h1>Table of Contents<span class="tocSkip"></span></h1>
# <div class="toc"><ul class="toc-item"></ul></div>

# %%
import pandas as pd
import numpy as np

def calculate_machines_needed(users, mem_per_user, active_machine):
    memory_per_machine = active_machine['Memory']
    total_gigs_needed = users * mem_per_user
    total_machines_needed = int(np.ceil(total_gigs_needed / memory_per_machine))
    return total_machines_needed

n1_machines=pd.read_csv('n1_machines.csv',index_col='Machine type')
active_machine = n1_machines.loc['n1-standard-8']
machine_cost=active_machine['Price (USD / hr)']*24. #cost per day per machine
num_machines=calculate_machines_needed(100,2,active_machine)

disks = pd.read_csv('disks.csv',index_col="Type")
disk_cost=disks.loc['Standard provisioned space']['Price (per GB / month)']/30.  #Gbyte/day

# %%
disks

# %%
n1_machines
