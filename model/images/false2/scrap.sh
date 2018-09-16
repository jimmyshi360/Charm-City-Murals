#!/bin/bash

# The commands to replicate this dataset. Images not actually provided for
# licensing issues.
pip install --user google_images_download
google_images_download -k "grey brick building" -l 150 -fjpg
