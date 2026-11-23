
from core.config_manager import ConfigManager


def test_config_save_and_load(tmp_path):

    manager = ConfigManager(tmp_path)

    settings = {
        "polling_rate": 50,
        "deadzone": 0.10
    }

    manager.save("test.yaml", settings)

    loaded = manager.load("test.yaml")

    assert loaded == settings


def test_missing_config():

    manager = ConfigManager("nonexistent_config_folder")

    try:
        manager.load("missing.yaml")

    except FileNotFoundError:
        assert True

    else:
        assert False, "Expected FileNotFoundError"
