#!/bin/bash

cd $( dirname ${BASH_SOURCE} )

set -e

# slc6 (all rhel-based with python 2.6)
./create-packs.sh --python-version 2.6 --iteration 1 --verbose --targets rpm --suffix py26

# fedora20 (all rhel-based with python 2.7)
./create-packs.sh --python-version 2.7 --iteration 1 --verbose --targets rpm --suffix py27

# ubuntu (all deb-based with python 2.7)
./create-packs.sh --python-version 2.7 --iteration 1 --verbose --targets deb --suffix py27

echo -e "\033[32mAll packages created successfully\033[m"
