# fuzzing
timeout 43200 $AFL_DIR/afl-fuzz -C -d -m none -i $PWD/seed -o $AFL_WORKDIR -- $EVAL_DIR/mruby_fuzz @@

# move crashes to eval dir
cp $AFL_WORKDIR/queue/* $EVAL_DIR/inputs/crashes

# move non-rashes to eval dir
cp $AFL_WORKDIR/non_crashes/* $EVAL_DIR/inputs/non_crashes
