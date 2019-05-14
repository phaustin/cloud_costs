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
#   toc:
#     base_numbering: 1
#     nav_menu: {}
#     number_sections: true
#     sideBar: true
#     skip_h1_title: false
#     title_cell: Table of Contents
#     title_sidebar: Contents
#     toc_cell: false
#     toc_position: {}
#     toc_section_display: true
#     toc_window_display: false
# ---

# %% [markdown]
# # JupyterHub cost estimator
#
# This will help you estimate the cost of running a JupyterHub for your purposes. Costs vary along many dimensions, such as the cloud provider used, the location from which you're running machines, and the types of machines you require.
#
# Below are the standard prices for a Google Cloud instance running from Oregon. They should give you a general idea of how much your hub will cost.
#
# Here's a list of available machine types. For more information see the [Google Cloud pricing guide](https://cloud.google.com/compute/pricing).

# %% {"scrolled": false}
from z2jh import cost_display, disk, machines
machines

# %% [markdown]
# Next, run this cell to determine your cost. It will display a widget that lets you draw a pattern of typical usage (you can control the amount of time that is shown with the `n_days` parameter).
#
# Play around with different machine configurations to see how this would affect the cost of your deployment.

# %%
fig = cost_display(n_days=7)
