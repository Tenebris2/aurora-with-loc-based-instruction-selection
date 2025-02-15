objdump -dGlS $1 > trace.dump
OUTPUT_FILE="source_code_extraction_time.txt"
{ time python3 ./scripts/extract_addresses.py trace.dump; } 2> "$OUTPUT_FILE"

cp addresses $AURORA_GIT_DIR/tracing/scripts/ -r
