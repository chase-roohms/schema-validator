import argparse
import os

from pprint import pp
from data_load import DataLoader
from jsonschema import validate, ValidationError, SchemaError
from lxml import etree

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
    # Print parsed arguments for debugging
    print("Parsed arguments:")
    pp(vars_args)

    # Set files to validate
    if vars_args['files']:
        vars_args['files'] = [f for f in vars_args['files'].splitlines()]
    else:
        # Find files based on file-format
        format_extensions = {
            'yaml': ['.yaml', '.yml'],
            'json': ['.json'],
            'xml': ['.xml', '.xsd']
        }
        extensions = format_extensions.get(vars_args['file_format'], [f".{vars_args['file_format']}"])
        vars_args['files'] = [f for f in os.listdir('.') if any(f.endswith(ext) and f != os.path.abspath(vars_args['schema_file']) for ext in extensions)]
    
    # Save dictionary with the filepaths as keys and the data from each file as values
    files_to_validate = {
        f: DataLoader.load_file(f, vars_args['file_format']) for f in vars_args['files']
    }

    # Set schema data
    if vars_args['schema_file']:
        schema_file_path = os.path.abspath(vars_args['schema_file'])
        # Determine if it's an XSD schema or JSON Schema
        if schema_file_path.endswith('.xsd'):
            # For XSD, load the schema using DataLoader
            schema_data = DataLoader.load_xsd_file(schema_file_path)
            is_xsd = True
        else:
            schema_data = DataLoader.load_file(schema_file_path, vars_args['schema_format'])
            is_xsd = False
    elif vars_args['schema_url']:
        # Check if the URL points to an XSD file
        if vars_args['schema_url'].endswith('.xsd'):
            schema_data = DataLoader.load_xsd_url(vars_args['schema_url'])
            is_xsd = True
        else:
            schema_data = DataLoader.load_url(vars_args['schema_url'], vars_args['schema_format'])
            is_xsd = False
    else:
        is_xsd = False
    
    error_dict = dict()
    # Validate files against schema
    for file_path, file_data in files_to_validate.items():
        try:
            if is_xsd:
                # Validate XML against XSD (schema_data is already an XMLSchema object)
                with open(file_path, 'rb') as xml_file:
                    xml_doc = etree.parse(xml_file)
                if schema_data.validate(xml_doc):
                    print(f"File {file_path} is valid.")
                else:
                    print(f"File {file_path} is invalid: {schema_data.error_log}")
                    error_dict[file_path] = schema_data.error_log
            else:
                # Validate using JSON Schema (works for JSON and YAML after parsing)
                validate(instance=file_data, schema=schema_data)
                print(f"File {file_path} is valid.")
        except (SchemaError, etree.DocumentInvalid) as e:
            raise
        except ValidationError as e:
            print(f"File {file_path} validation error: {e}")
            error_dict[file_path] = str(e)
    
    if len(error_dict) > 0:
        print("Validation errors found:")
        for file_path, error in error_dict.items():
            print(f"::error::{file_path} not valid")
            print(error)
        quit(1)

if __name__ == "__main__":
    main()