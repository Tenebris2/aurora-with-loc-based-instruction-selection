#!/bin/bash 

#2
rm $EVAL_DIR/*_trace

cp $EVAL_DIR/test_bin/1-readelf/readelf_trace $EVAL_DIR 

python3 fuzzing.py $EVAL_DIR/seed/readelf_seed/  "$EVAL_DIR/test_bin/1-readelf/readelf_fuzz -a @@"

python3 run.py "$EVAL_DIR/matdump_trace @@" "readelf.c:16197"

#3
rm $EVAL_DIR/*_trace

cp $EVAL_DIR/test_bin/4-sleuthkit/fls_trace $EVAL_DIR 

python3 fuzzing.py $EVAL_DIR/seed/sleuthkit_seed/  "$EVAL_DIR/test_bin/4-sleuthkit/fls_fuzz @@"

python3 run.py "$EVAL_DIR/fls_trace @@" "ext2fs.c:807"

#4

rm $EVAL_DIR/*_trace

cp $EVAL_DIR/test_bin/5-lua/lua_trace $EVAL_DIR

python3 fuzzing.py $EVAL_DIR/seed/lua_seed/ "$EVAL_DIR/test_bin/5-lua/lua_fuzz @@"

python3 run.py "$EVAL_DIR/lua_trace @@" "ldo.c:325"

#5
rm $EVAL_DIR/*_trace

cp $EVAL_DIR/test_bin/7-libsixel/img2sixel_trace $EVAL_DIR

python3 fuzzing.py $EVAL_DIR/seed/libsixel_seed/ "$EVAL_DIR/test_bin/7-libsixel/img2sixel_fuzz @@"

python3 run.py "$EVAL_DIR/img2sixel_trace @@" "stb_image.h:6110"

#6
rm $EVAL_DIR/*_trace

cp $EVAL_DIR/test_bin/10-nm_stack_overflow/nm_trace $EVAL_DIR

python3 fuzzing.py $EVAL_DIR/seed/nm_seed/ "$EVAL_DIR/test_bin/10-nm_stack_overflow/nm_fuzz -n @@"

python3 run.py "$EVAL_DIR/nm_trace -n @@" "tekhex.c:276"

#7

rm $EVAL_DIR/*_trace

cp $EVAL_DIR/test_bin/12-libzip/ziptool_trace $EVAL_DIR

python3 fuzzing.py $EVAL_DIR/seed/ziptool_seed/ "$EVAL_DIR/test_bin/12-libzip/ziptool_fuzz @@ cat index"

python3 run.py "$EVAL_DIR/ziptool_trace @@ cat index" "zip_dirent.c:580"

#8: RUST BACKTRACE

rm $EVAL_DIR/*_trace

cp $EVAL_DIR/test_bin/15-libjpeg_divide_by_zero/cjpeg_divide_by_zero_trace $EVAL_DIR

python3 fuzzing.py $EVAL_DIR/seed/libjpeg_divide_by_zero/ "$EVAL_DIR/test_bin/15-libjpeg_divide_by_zero/cjpeg_divide_by_zero_fuzz @@"

python3 run.py "$EVAL_DIR/cjpeg_divide_by_zero_trace @@" "rdgif.c:447"

#9

rm $EVAL_DIR/*_trace

cp $EVAL_DIR/test_bin/16-libjpeg_heap_buffer_overflow/cjpeg_heap_buffer_overflow_trace $EVAL_DIR

python3 fuzzing.py $EVAL_DIR/seed/libjpeg_heap_buffer_overflow/ "$EVAL_DIR/test_bin/16-libjpeg_heap_buffer_overflow/cjpeg_heap_buffer_overflow_fuzz -outfile /dev/null @@"

python3 run.py "$EVAL_DIR/cjpeg_heap_buffer_overflow_trace -outfile /dev/null @@" "rdbmp.c:209"

