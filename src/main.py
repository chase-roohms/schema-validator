import argparse
import os

from pprint import pp

from data_load.data_load import DataLoader

def get_file_dict_list(files, file_format: str = None):
    return [DataLoader.load_file(f, file_format) for f in files]

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

    # Replace empty strings with None
    for key, value in vars_args.items():
        if value == '':
            vars_args[key] = None
    # Print parsed arguments
    print("Parsed arguments:")
    pp(vars_args)

    # Set files to validate
    if vars_args['files']:
        vars_args['files'] = [os.path.abspath(f) for f in vars_args['files'].splitlines()]
    else:
        # Find files based on file-format
        format_extensions = {
            'yaml': ['.yaml', '.yml'],
            'json': ['.json'],
            'xml': ['.xml']
        }
        extensions = format_extensions.get(vars_args['file_format'], [f".{vars_args['file_format']}"])
        vars_args['files'] = [os.path.abspath(f) for f in os.listdir('.') if any(f.endswith(ext) for ext in extensions)]
    files_to_validate = [
        DataLoader.load_file(f, vars_args['file_format']) for f in vars_args['files']
    ]

    # Set schema data
    if vars_args['schema_file']:
        schema_data = DataLoader.load_file(os.path.abspath(vars_args['schema_file']), vars_args['schema_format'])
    elif vars_args['schema_url']:
        schema_data = DataLoader.load_url(vars_args['schema_url'], vars_args['schema_format'])

    pp(files_to_validate)
    pp(schema_data)

if __name__ == "__main__":
    main()