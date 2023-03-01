import argparse

from typing import List

from utils import *


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Test VM assembler/disassembler roundtrip.')
    parser.add_argument('--root', metavar='ROOT', type=str, dest='root_dir', \
                        required=False, default='tests', \
                        help='root directory for in/vm/*.vmasm')
    return parser.parse_args()


def execute_test(name: str, in_vmasm: str, ref_sys_enter: str, ref_vmasm: str, out_hex: str, out_lbl: str, out_vmasm: str):
    print(f"{name}...", end='')

    if not execute(f"cp {ref_sys_enter} {ref_vmasm}"):
        print_red('failed')
        return
    if not execute(f"python3 $UCOMP_DEVROOT/tests/bin/fstrip.py < {in_vmasm} >> {ref_vmasm}"):
        print_red('failed')
        return
    if not execute(f"python3 $UCOMP_DEVROOT/tools/vmasm.py -o {out_hex} -l {out_lbl} {in_vmasm}"):
        print_red('failed')
        return
    if not execute(f"python3 $UCOMP_DEVROOT/tools/vmdisasm.py -o {out_vmasm} -l {out_lbl} {out_hex}"):
        print_red('failed')
        return
    if not execute(f"diff {ref_vmasm} {out_vmasm}"):
        print_red('failed')
        return
    
    print_green('pass')


def execute_tests():
    args: argparse.Namespace = parse_args()

    in_dir: str                             = f"{args.root_dir}/in/vm"
    ref_dir: str                            = f"{args.root_dir}/ref"
    out_dir: str                            = create_tmpdir('vmasm2vmasm-')

    names: List[str]                        = [f"{file.rpartition('.')[0]}" for file in list_files(in_dir, '.vmasm')]
    in_vmasm_files: List[str]               = [f"{in_dir}/{name}.vmasm" for name in names]
    out_hex_files: List[str]                = [f"{out_dir}/{name}.hex" for name in names]
    out_lbl_files: List[str]                = [f"{out_dir}/{name}.lbl" for name in names]
    out_vmasm_files: List[str]              = [f"{out_dir}/{name}.vmasm" for name in names]

    ref_sys_enter: str                      = f"{ref_dir}/sys_enter.vmasm"
    ref_vmasm: str                          = f"{out_dir}/ref.vmasm"

    tests: zip[tuple[str, str, str, str, str]] \
        = zip(names, in_vmasm_files, out_hex_files, out_lbl_files, out_vmasm_files)

    print_green("*.vmasm -> *.{hex,lbl} -> *.vmasm")
    for name, in_vmasm, out_hex, out_lbl, out_vmasm in tests:
        execute_test(name, in_vmasm, ref_sys_enter, ref_vmasm, out_hex, out_lbl, out_vmasm)
    
    remove_dir(out_dir)


execute_tests()
