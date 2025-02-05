import json
from pathlib import Path


def format_number(value: float) -> str:
    """Formats a numeric value to a string with two decimal places."""
    value = float(value)
    return f"{value:.2f}".rstrip('0').rstrip('.')


def load_json_test_data(filename: str):
    file_path = Path(__file__).parent / 'data' / filename
    with file_path.open(encoding="utf-8") as f:
        data = json.load(f)
        return data
    
    
def load_json_test_data_comment(filename: str):
    file_path = Path(__file__).parent / 'data' / filename
    with file_path.open(encoding="utf-8") as f:
        data = json.load(f)
    return [
        (item["input_value"], item["expected_value"], item.get("comment", ""))
        for item in data
    ]
    
    
class Translations:
    LANGUAGE = "en"  # Default language
    _translations = None  # Translations cache

    @classmethod
    def load_translations(cls):
        if cls._translations is None:
            file_path = Path(__file__).parent / "data" / "translations.json"
            if not file_path.exists():
                raise FileNotFoundError(f"Translations file not found: {file_path}")
            with file_path.open(encoding="utf-8") as f:
                cls._translations = json.load(f)
        return cls._translations

    @classmethod
    def get_label(cls, group, key):
        translations = cls.load_translations()
        return translations.get(cls.LANGUAGE, {}).get(group, {}).get(key, key)

    @classmethod
    def get_group(cls, group):
        translations = cls.load_translations()
        return translations.get(cls.LANGUAGE, {}).get(group, {})