import os

ENV = os.getenv("ENV", "test")

def get_db_path():
    if ENV == "prod":
        return "csra.db"
    else:
        return "csra_test.db"