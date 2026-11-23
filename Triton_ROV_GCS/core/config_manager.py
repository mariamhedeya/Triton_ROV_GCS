
import yaml
from pathlib import Path


class ConfigManager:

    def __init__(self, config_directory="config"):
        self.config_directory = Path(config_directory)

    def load(self, filename):

        file_path = self.config_directory / filename

        if not file_path.exists():
            raise FileNotFoundError(
                f"Configuration not found: {file_path}"
            )

        with open(file_path, "r", encoding="utf-8") as file:
            data = yaml.safe_load(file)

        if not isinstance(data, dict):
            raise ValueError(
                f"Invalid YAML configuration: {filename}"
            )

        return data

    def save(self, filename, data):

        self.config_directory.mkdir(
            parents=True,
            exist_ok=True
        )

        file_path = self.config_directory / filename

        with open(file_path, "w", encoding="utf-8") as file:
            yaml.safe_dump(
                data,
                file,
                sort_keys=False
            )
