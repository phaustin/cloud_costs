#!/bin/bash -v
rm -rf notebooks
mkdir -p notebooks
rsync -av ../*ipynb notebooks/.
rsync -av ../*csv notebooks/.
sphinx-build -v -N -b html .  _build
