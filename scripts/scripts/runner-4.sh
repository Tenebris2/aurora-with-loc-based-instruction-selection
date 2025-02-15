#!/bin/bash 

rm $EVAL_DIR/*_trace

cp $EVAL_DIR/test_bin/11-mruby_type_confusion/mruby_trace $EVAL_DIR 

python3 fuzzing.py $EVAL_DIR/seed/ruby_seed/ "$EVAL_DIR/test_bin/11-mruby_type_confusion/mruby_fuzz @@"

python3 run.py "$EVAL_DIR/mruby_trace" "error.c:277"

#15

rm $EVAL_DIR/*_trace

cp $EVAL_DIR/test_bin/13-mruby_integer_overflow/mruby_integer_overflow_trace $EVAL_DIR 

python3 fuzzing.py $EVAL_DIR/seed/mruby_integer_overflow_seed/ "$EVAL_DIR/test_bin/13-mruby_integer_overflow/mruby_integer_overflow_fuzz @@"

python3 run.py "$EVAL_DIR/mruby_integer_overflow_trace @@" "vm.c:1234"

