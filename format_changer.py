
import argparse


def main():
    parser = argparse.ArgumentParser(description="Data File Handler")
    parser.add_argument("input_files", nargs=2, help="Input files and formats")
    args = parser.parse_args()

    input_files = args.input_files




if __name__ == "__main__":
    main()