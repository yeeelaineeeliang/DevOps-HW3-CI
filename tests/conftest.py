# flake8: noqa

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import pytest
from app import create_app


@pytest.fixture
def app(tmp_path):
    app = create_app()

    data_dir = tmp_path / "data"
    data_dir.mkdir(parents=True, exist_ok=True)

    app.config["DATA_DIR"] = str(data_dir)
    app.config["TESTING"] = True

    return app


@pytest.fixture
def client(app):
    return app.test_client()
