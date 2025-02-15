# How to run the example

## Installing Ghidra

Install Ghidra using this link: https://ghidra-sre.org/InstallationGuide.html

Then run 'export GHIDRA_INSTALL_DIR=${THE_GHIDRA_FOLDER_YOU_INSTALLED}'

## Running the example

### Exporting

``` bash
export AURORA_GIT_DIR=$PWD/aurora/
export EVAL_DIR=$PWD/evaluation/
export AFL_DIR=$PWD/evaluation/afl-fuzz/
export AFL_WORKDIR=$PWD/evaluation/afl-workdir/
export PIN_ROOT=$PWD/evaluation/pin-3.15-98253-gb56e429b1-gcc-linux/
```

### Running the scripts

Run the scripts in order: 

build_trace -> build_fuzz -> prepare_fuzzing -> run_fuzz -> setup_decompiling -> run_trace -> run_rca
