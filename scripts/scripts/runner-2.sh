#!/bin/bash 

#1: RUST BACKTRACE
# rm $EVAL_DIR/*_trace
#
# cp $EVAL_DIR/test_bin/0-matio/matdump_trace $EVAL_DIR 
#
# python3 fuzzing.py $EVAL_DIR/seed/matio_seed/  "$EVAL_DIR/test_bin/0-matio/matdump_fuzz @@"
#
# python3 run.py "$EVAL_DIR/matdump_trace @@" "mat5.c:4975"

#8: RUST BACKTRACE

# rm $EVAL_DIR/*_trace
#
# cp $EVAL_DIR/test_bin/15-libjpeg_divide_by_zero/cjpeg_divide_by_zero_trace $EVAL_DIR
#
# python3 fuzzing.py $EVAL_DIR/seed/libjpeg_divide_by_zero/ "$EVAL_DIR/test_bin/15-libjpeg_divide_by_zero/cjpeg_divide_by_zero_fuzz @@"
#
# python3 run.py "$EVAL_DIR/cjpeg_divide_by_zero_trace @@" "rdgif.c:447"
#

#10

rm $EVAL_DIR/*_trace

cp $EVAL_DIR/test_bin/17-libpng/pngimage_trace $EVAL_DIR 

python3 fuzzing.py $EVAL_DIR/seed/libpng_seed/ "$EVAL_DIR/test_bin/17-libpng/pngimage_fuzz @@"

python3 run.py "$EVAL_DIR/pngimage_trace @@" "pngrutil.c:3152"

#11

rm $EVAL_DIR/*_trace

cp $EVAL_DIR/test_bin/18-libxml2/xmllint_trace $EVAL_DIR 

python3 fuzzing.py $EVAL_DIR/seed/libxml2_seed/ "$EVAL_DIR/test_bin/18-libxml2/xmllint_fuzz --recover @@"

python3 run.py "$EVAL_DIR/xmllint_trace --recover @@" "valid.c:1181"

#12 

rm $EVAL_DIR/*_trace

cp $EVAL_DIR/test_bin/19-tcpdump/tcpdump_trace $EVAL_DIR 

python3 fuzzing.py $EVAL_DIR/seed/tcpdump_seed/ "$EVAL_DIR/test_bin/19-tcpdump/tcpdump_fuzz -vr @@"

python3 run.py "$EVAL_DIR/tcpdump_trace -vr @@" "print-aoe.c:328"

#13

rm $EVAL_DIR/*_trace

cp $EVAL_DIR/test_bin/22-ezXML/ezxml_trace $EVAL_DIR 

python3 fuzzing.py $EVAL_DIR/seed/ezxml_seed/ "$EVAL_DIR/test_bin/22-ezXML/ezxml_fuzz @@"

python3 run.py "$EVAL_DIR/ezxml_trace @@" "ezxml.c:362"

