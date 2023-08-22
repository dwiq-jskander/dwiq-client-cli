import os

from dotenv import load_dotenv

dir_path = os.path.dirname(os.path.realpath(__file__))
env_file = f"{dir_path}/../../.env"
if os.path.isfile(env_file):
    load_dotenv(env_file)


class Configuration:
    project = os.getenv("GOOGLE_CLOUD_PROJECT")
    bq_dataset = os.getenv("BQ_DATASET")


config = Configuration()
