from re import sub
import shutil
import threading
import subprocess
import sys
import os

TIME_OUT = 60 * 60
threads = []
# env
afl_dir = os.getenv("AFL_DIR")
afl_workdir = os.getenv("AFL_WORKDIR")
eval_dir = os.getenv("EVAL_DIR")
print(afl_dir)
print(afl_workdir)

# example: python3 fuzzing.py $EVAL_DIR/seed/matio_seed/ "$EVAL_DIR/matdump_trace @@"
seed_input = sys.argv[1]
arg = sys.argv[2]


def run(id: int, seed: str, args: str):
    cleanup(id)
    # cmd = f"./test.sh {id} {seed} {args}"
    cmd = f"timeout {TIME_OUT} {afl_dir}afl-fuzz -C -d -m none -i {seed} -o {afl_workdir}afl-workdir-{id} -- {args}"
    print(cmd)
    res = subprocess.run(cmd, shell=True, text=True, capture_output=True)
    print(res.stdout, res.stderr)
    move(id)


def cleanup(id: int):
    input_rm = f"rm -rf {eval_dir}/inputs/input-{id}/*"

    workdir_rm = f"rm -rf {afl_workdir}/afl-workdir-{id}/*"
    print(input_rm)

    input_res = subprocess.run(input_rm, shell=True, text=True, capture_output=True)
    print(input_res.stdout, input_res.stderr)
    workdir_res = subprocess.run(workdir_rm, shell=True, text=True, capture_output=True)
    print(workdir_res.stdout, workdir_res.stderr)


def main():
    # threaded
    for t in range(0, 5):
        # run(t, sys.argv[1], sys.argv[2])

        thread = threading.Thread(target=run, args=[t, sys.argv[1], sys.argv[2]])
        thread.start()


def move(id):
    mv_cmd = f"cp {afl_workdir}afl-workdir-{id}/crashes {afl_workdir}afl-workdir-{id}/non_crashes -r {eval_dir}/inputs/input-{id}"
    print(mv_cmd)
    mv_res = subprocess.run(mv_cmd, shell=True, text=True, capture_output=True)
    print(mv_res.stdout, mv_res.stderr)


if __name__ == "__main__":
    main()
