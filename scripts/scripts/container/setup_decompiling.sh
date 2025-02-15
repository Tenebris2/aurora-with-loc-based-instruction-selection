#!/bin/bash

export GHIDRA_INSTALL_DIR=~/Disk/Tools/ghidra_11.1.2_PUBLIC/

# Define the output file
OUTPUT_FILE="decompiling_execution_time.txt"

# Run the Python script and measure the time
{ time (python3 ./decompiler/pydra.py "$1" &&  python3 ./decompiler/extract.py)} 2> "$OUTPUT_FILE"

cp addresses $AURORA_GIT_DIR/tracing/scripts
