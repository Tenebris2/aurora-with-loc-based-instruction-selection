import enum
import os
import shutil
import subprocess
import sys
from enum import Enum
from extract_ranking import extract_ranking

# Env Vars
eval_dir = os.getenv("EVAL_DIR")
aurora_git_dir = os.getenv("AURORA_GIT_DIR")
afl_workdir = os.getenv("AFL_WORKDIR")
afl_dir = os.getenv("AFL_DIR")
pin_root = os.getenv("PIN_ROOT")
method_dir = os.getenv("METHOD_DIR")

# Arg: "$EVAL_DIR/readelf_trace readelf.c:16197"
args = sys.argv[1]
target = sys.argv[2]
fpath = args.split("/")
temp = args.split(" ")[0].split("/")[-1]
fpath = f"{eval_dir}/results/{temp}"
AURORA_PATH = f"{fpath}/aurora/"
LOC_PATH = f"{fpath}/loc/"
LOC_WITH_SOURCE_PATH = f"{fpath}/loc_with_source/"
BASIC_BLOCK_PATH = f"{fpath}/basic_block/"
SCRIPT_PATH = f"{aurora_git_dir}/tracing/scripts"
TRACES_PATH = f"{eval_dir}/traces"
RCA_PATH = f"{aurora_git_dir}/root_cause_analysis"
DECOMPILING_RESULTS = f"{os.getcwd()}/decompiling_execution_time.txt"
SOURCE_CODE_EXTRACTION_RESULTS = (
    f"{os.getcwd()}/source-code-extractor/source_code_extraction_time.txt"
)
HIT_COUNT = "hitcount.out"
paths = [AURORA_PATH, LOC_PATH, LOC_WITH_SOURCE_PATH, BASIC_BLOCK_PATH]
for path in paths:
    os.makedirs(path, exist_ok=True)
paths = [AURORA_PATH, LOC_PATH, LOC_WITH_SOURCE_PATH, BASIC_BLOCK_PATH]


class Method(Enum):
    AURORA = f"{method_dir}/default_tracing/aurora_tracer.cpp"
    LOC = f"{method_dir}/map_tracing/aurora_tracer.cpp"
    BASIC_BLOCK = f"{method_dir}/jump_tracing/aurora_tracer.cpp"


# results -> stats from traces, predicate ranking, line ranking, rca time
def setup():
    # arguments, binary
    arguments = " ".join(args.split(" ")[1:])
    print(arguments)
    with open(f"{eval_dir}/arguments.txt", "w") as file:
        file.write(arguments)


# aurora
def run(method: Method, with_source: bool, id: int):
    res_path = ""
    if method == method.AURORA:
        res_path = AURORA_PATH + f"aurora_{id}"
    elif method == Method.LOC:
        if with_source == True:
            res_path = LOC_WITH_SOURCE_PATH + f"loc_with_source_{id}"
        else:
            res_path = LOC_PATH + f"loc_{id}"
    elif method == Method.BASIC_BLOCK:
        res_path = BASIC_BLOCK_PATH + f"basic_block_{id}"
    os.makedirs(res_path, exist_ok=True)
    trace(res_path, method=method, with_source=with_source, id=id)
    root_cause_analysis(res_path)


def print_res(cmd):
    print(cmd.stdout, cmd.stderr)


def trace(res_path, method: Method, with_source: bool, id: int):
    clean_previous_run()

    # move input-{id} into input directory for rca monitoring
    move_input_cmd = f"cp {eval_dir}/inputs/input-{id}/* -r {eval_dir}/inputs/"
    subprocess.run(move_input_cmd, shell=True, text=True, capture_output=True)
    set_method(method, with_source)
    trace_cmd = f'python3 {SCRIPT_PATH}/tracing.py "{args}" {eval_dir}/inputs/input-{id} {eval_dir}/traces'
    print(trace_cmd)
    trace_cmd_res = subprocess.run(
        trace_cmd, shell=True, text=True, capture_output=True
    )
    print_res(trace_cmd_res)

    get_addr_cmd = (
        f"python3 {SCRIPT_PATH}/addr_ranges.py --eval_dir {eval_dir} {TRACES_PATH}"
    )
    get_addr_cmd_res = subprocess.run(
        get_addr_cmd, shell=True, text=True, capture_output=True
    )
    print_res(get_addr_cmd_res)

    try:
        shutil.copy(f"{TRACES_PATH}/stats.txt", res_path)
        if method == Method.LOC and with_source == False:
            move_decompiling_results(id)
        elif method == Method.LOC and with_source == True:
            move_source_code_extraction_results(id)
        shutil.copy(f"{os.getcwd()}/{HIT_COUNT}", res_path)
        print(f"File moved from {TRACES_PATH} to {res_path}")
        print(f"File {os.getcwd()}/{HIT_COUNT} move to {res_path}")
    except FileNotFoundError:
        print(f"Error: the file {TRACES_PATH} does not exist")


def clean_previous_run():
    if os.path.exists("/tmp/tm"):
        print(f"/tmp/tm exists")
        shutil.rmtree("/tmp/tm")
    rm_traces_cmd = f"rm -rf {TRACES_PATH}/*"
    subprocess.run(rm_traces_cmd, shell=True)
    print("Cleaned")
    rm_trace_ghidras = f"rm -rf {eval_dir}/*_trace_ghidra"
    subprocess.run(rm_trace_ghidras, shell=True)
    try:
        os.remove(f"{os.getcwd()}/{HIT_COUNT}")
    except FileNotFoundError:
        print("Hit count not found")


def cleanup():
    rm_trace_binaries = f"rm {eval_dir}/*_trace"
    subprocess.run(rm_trace_binaries, shell=True)


def root_cause_analysis(res_path: str):
    # run rca
    rca_cmd = f"cargo run --release --bin rca -- --eval-dir {eval_dir} --trace-dir {eval_dir} --monitor --rank-predicates"
    # enrich
    addr2bin_cmd = f"cargo run --release --bin addr2line -- --eval-dir {eval_dir}"
    result = subprocess.run(
        rca_cmd, shell=True, text=True, capture_output=True, cwd=RCA_PATH
    )
    subprocess.run(
        addr2bin_cmd, shell=True, text=True, capture_output=True, cwd=RCA_PATH
    )
    print_res(result)
    predicate_rank, line_rank = extract_ranking(
        f"{eval_dir}/ranked_predicates_verbose.txt", target
    )

    with open(f"{res_path}/rca_results.txt", "w") as file:
        file.write(result.stdout)
        file.write(result.stderr)
        file.write(f"Predicate Ranking: {predicate_rank}\n LOC Ranking: {line_rank}")
    try:
        shutil.copy(f"{eval_dir}/ranked_predicates_verbose.txt", res_path)
    except FileNotFoundError:
        print("File ranked_predicates_verbose.txt could not be found")


def set_method(method: Method, with_source: bool):
    setup_method_cmd = f"{method_dir}/setup_method.sh " + method.value
    print(setup_method_cmd)
    if method == Method.AURORA or method == Method.BASIC_BLOCK:
        print(setup_method_cmd)
    elif method == Method.LOC:
        if with_source == False:
            setup_address_cmd = f"./setup_decompiling.sh {eval_dir}/*_trace"
            print(setup_address_cmd)

            set_addr_res = subprocess.run(
                setup_address_cmd,
                shell=True,
                text=True,
                capture_output=True,
                cwd=f"{os.getcwd()}",
            )
            print(set_addr_res.stdout, set_addr_res.stderr)
        else:
            setup_address_cmd = f"./extract.sh {eval_dir}/*_trace"
            print(args)
            print(setup_address_cmd)
            set_addr_res = subprocess.run(
                setup_address_cmd,
                shell=True,
                text=True,
                capture_output=True,
                cwd=f"{os.getcwd()}/source-code-extractor/",
            )
            print(set_addr_res.stdout, set_addr_res.stderr)
    set_method_res = subprocess.run(
        setup_method_cmd, shell=True, text=True, capture_output=True
    )
    print(f"Setting method: {set_method_res.stdout} {set_method_res.stderr}")


def move_decompiling_results(id):
    try:
        shutil.copy(DECOMPILING_RESULTS, f"{LOC_PATH}/loc_{id}/")
        print(f"Moved {DECOMPILING_RESULTS} to {LOC_PATH}/loc_{id}")
    except FileNotFoundError:
        print(f"{DECOMPILING_RESULTS} not found")
    except shutil.Error as e:
        print(f"Shutil error: {e}")


def move_source_code_extraction_results(id):
    try:
        shutil.copy(
            SOURCE_CODE_EXTRACTION_RESULTS,
            f"{LOC_WITH_SOURCE_PATH}/loc_with_source_{id}/",
        )
        print(
            f"Moved {SOURCE_CODE_EXTRACTION_RESULTS} to {LOC_WITH_SOURCE_PATH}/loc_with_source_{id}"
        )
    except FileNotFoundError:
        print(f"{SOURCE_CODE_EXTRACTION_RESULTS} not found")
    except shutil.Error as e:
        print(f"Shutil error: {e}")


setup()
for i in range(0, 5):
    run(Method.AURORA, False, i)
    run(Method.LOC, False, i)
    run(Method.LOC, True, i)
    run(Method.BASIC_BLOCK, False, i)
