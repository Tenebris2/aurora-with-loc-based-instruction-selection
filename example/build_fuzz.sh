#!/bin/bash


cd mruby
make clean

# build instrument version for fuzzing
CC=$AFL_DIR/afl-gcc CFLAGS="-g -O0 -fPIC -fsanitize=address"  LDFLAGS="-fsanitize=address -fPIC -lm" LD=$CC ./minirake  $PWD/bin/mruby
mv $PWD/bin/mruby $EVAL_DIR/mruby_fuzz

mv $PWD/bin/mruby $EVAL_DIR/mruby_fuzz
