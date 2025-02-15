#!/bin/bash

#8: RUST BACKTRACE

rm $EVAL_DIR/*_trace

cp $EVAL_DIR/test_bin/15-libjpeg_divide_by_zero/cjpeg_divide_by_zero_trace $EVAL_DIR

python3 fuzzing.py $EVAL_DIR/seed/libjpeg_divide_by_zero/ "$EVAL_DIR/test_bin/15-libjpeg_divide_by_zero/cjpeg_divide_by_zero_fuzz @@"

python3 run.py "$EVAL_DIR/cjpeg_divide_by_zero_trace @@" "rdgif.c:447"

