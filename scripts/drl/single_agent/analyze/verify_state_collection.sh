#!/bin/bash

cd "$(dirname "$0")/../../../.." || exit

python analysis/drl/single_agent/verify_state_collection.py
