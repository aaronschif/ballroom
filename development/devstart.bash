#/bin/bash

# Bootstrap development 
# =====================
#
# Source in base directiory, run once.

git submodule init
git pull

pip install -r development/py_requirements.pip
