#!/usr/bin/env python3
import argarse

# -------------------- Argparse --------------------


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-h", type=str, help="description of the argumet")
    return parser.parse_args()


# -------------------- Main --------------------


def main(parsed_args):
    return


# -------------------- Start Here --------------------

if __name__ == "__main__":
    parsed_args = parse_arguments()
    main(parsed_args)
