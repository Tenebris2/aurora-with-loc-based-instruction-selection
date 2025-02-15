#!/bin/bash 

rm $EVAL_DIR/*_trace

cp $EVAL_DIR/test_bin/20-patch/patch_trace $EVAL_DIR 

python3 fuzzing.py $EVAL_DIR/seed/patch_seed/  "$EVAL_DIR/test_bin/20-patch/patch_fuzz  -o outfile -Rf"

python3 run.py "$EVAL_DIR/patch_trace -o outfile -Rf" "pch.c:1332"


