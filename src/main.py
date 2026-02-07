import argparse
from pprint import pp

def main():
    parser = argparse.ArgumentParser(
        description="Schema Validator",
        formatter_class=lambda prog: argparse.HelpFormatter(
            prog, max_help_position=40, width=120)
    )
    parser.add_argument("--files", type=str, help="files to validate")
    parser.add_argument("--file-format", type=str, help="file format")
    parser.add_argument("--schema-file", type=str, help="schema file")
    parser.add_argument("--schema-url", type=str, help="schema URL")
    parser.add_argument("--schema-format", type=str, help="schema format")
    parser.add_argument("--output-format", type=str, help="output format")
    parser.add_argument("--output-file", type=str, help="output file")
    args = parser.parse_args()
    vars_args = vars(args)
    vars_args['files'] = vars_args['files'].splitlines() if vars_args['files'] else []
    pp(vars_args)

if __name__ == "__main__":
    main()