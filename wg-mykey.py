#!/usr/bin/env python3
import subprocess
import argparse
import sys

def run_attempts(prefix,
                 case_sensitive=False,
                 max_attempts=-1,
                 executable="wg",
                 cmd = "genkey"):
    if not case_sensitive:
        prefix = prefix.upper()
    prefix = prefix.encode("ascii")
    attempts_left = -1
    found = False
    key = ""
    while attempts_left:
        key = subprocess.check_output([executable, cmd])
        attempts_left -= 1
        if not case_sensitive:
            keyconv = key.upper()
        else:
            keyconv = key
        found = keyconv.startswith(prefix)
        if found:
            break
    if found:
        sys.stdout.buffer.write(key)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        "Generate Wireguard keys until one starts with your desired prefix")
    parser.add_argument("prefix", help="prefix to check for")
    parser.add_argument(
        "-m",
        "--max-attempts",
        help="maximum attempts at finding (-1 means \"try indefinitely\")",
        type=int,
        default=-1)
    parser.add_argument("-e",
                        "--wireguard-executable",
                        help="wireguard executable to use",
                        default="wg")
    parser.add_argument("-s",
                        "--wireguard-subcommand",
                        help="wireguard subcommand to run (e.g. genkey, genpsk)",
                        default="genkey")
    parser.add_argument("-c",
                        "--case-sensitive",
                        help="be case sensitive",
                        action="store_true")
    args = parser.parse_args()
    run_attempts(args.prefix,
                 args.case_sensitive,
                 max_attempts=args.max_attempts,
                 executable=args.wireguard_executable)
