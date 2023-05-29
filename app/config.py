from os import environ


class Settings:
    DB_NAME = "postgres"  # environ["DB_NAME"]
    DB_PASSWORD = "postgres"  # environ["DB_PASSWORD"]
    DB_HOST_NAME = "localhost"  # environ["DB_HOST_NAME"]
    DB_PORT = 5432  # environ["DB_PORT"]
    DB_USER = "postgres"  # environ["DB_USER"]
