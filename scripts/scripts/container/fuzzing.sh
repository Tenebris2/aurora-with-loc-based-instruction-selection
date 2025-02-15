
rm -rf $EVAL_DIR/inputs/*

rm -rf $AFL_WORKDIR/*
# fuzzing
timeout 3600 $AFL_DIR/afl-fuzz -C -d -m none -i $2 -o $AFL_WORKDIR -- $3 @@

# move crashes to eval dir
cp $AFL_WORKDIR/queue/* $EVAL_DIR/inputs/crashes

# move non-rashes to eval dir
cp $AFL_WORKDIR/non_crashes/* $EVAL_DIR/inputs/non_crashes


