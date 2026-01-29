import os
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


@pytest.fixture
def sample_inventory(app):
    inventory_path = os.path.join(app.config["DATA_DIR"], "current_inventory.txt")

    with open(inventory_path, "w") as f:
        f.write("978-0-7432-7356-5|The Great Gatsby|F. Scott Fitzgerald|available\n")
        f.write("978-0-452-28423-4|1984|George Orwell|available\n")
        f.write("978-0-452-28424-1|Animal Farm|George Orwell|checked_out\n")

    return True
