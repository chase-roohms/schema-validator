import yaml
import json
import xmltodict
import requests

class DataLoader:
    @staticmethod
    def load_file(file_path, file_format: str = None) -> dict:
        if not file_format:
            file_format = DataLoader.__get_file_format(file_path)
        loader = DataLoader.__determine_file_loader(file_format)
        if loader:
            return loader(file_path)
        raise ValueError(f"Unsupported file format: {file_format}")
  
    @staticmethod
    def load_url(url, file_format: str = None) -> dict:
        if not file_format:
            file_format = DataLoader.__get_file_format(url)
        loader = DataLoader.__determine_text_loader(file_format)
        response = requests.get(url)
        if loader:
            return loader(response.text)
        raise ValueError(f"Unsupported file format: {file_format}")

    @staticmethod
    def __get_file_format(file_path):
        format_map = {
            "yaml": "yaml",
            "yml": "yaml",
            "json": "json",
            "xml": "xml"
        }
        ext = file_path.split(".")[-1].lower()
        return format_map.get(ext, ext)

    @staticmethod
    def __determine_file_loader(file_format):
        loaders = {
            "yaml": DataLoader.__load_yaml,
            "json": DataLoader.__load_json,
            "xml": DataLoader.__load_xml,
        }
        return loaders.get(file_format)
    
    @staticmethod
    def __determine_text_loader(file_format):
        loaders = {
            "yaml": yaml.safe_load,
            "json": json.loads,
            "xml": xmltodict.parse,
        }
        return loaders.get(file_format)

    @staticmethod
    def __load_yaml(file_path):
        with open(file_path, "r") as f:
            return yaml.safe_load(f)

    @staticmethod
    def __load_json(file_path):
        with open(file_path, "r") as f:
            return json.load(f)

    @staticmethod
    def __load_xml(file_path):
        with open(file_path, "r") as f:
            return xmltodict.parse(f.read())