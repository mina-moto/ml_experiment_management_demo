import os
import sys

import luigi
import mlflow
from dotenv import load_dotenv
from luigi.configuration import add_config_path, get_config

from tasks.prediction import Prediction
from tasks.preprocessor import Preprocessor
from tasks.trainer import Trainer


def main():
    load_dotenv()
    sys.path.append(f"{os.getenv('PROJECT_ROOT')}src/")
    add_config_path(os.getenv("LUIGI_CONFIG_PATH"))
    run_config = get_config(os.getenv("LUIGI_CONFIG_PARSER"))["RunConfig"]
    mlflow.set_experiment(run_config["experiment_name"])
    mlflow.start_run()
    mlflow.set_tag('mlflow.note.content', run_config["description"])
    mlflow.log_param("description", run_config["description"])
    mlflow.log_param("task", run_config["task"])
    mlflow.set_tag('mlflow.runName', mlflow.active_run().info.run_id)
    mlflow.log_artifact(os.getenv("LUIGI_CONFIG_PATH"))
    luigi.run([run_config["task"], "--local-scheduler"])
    mlflow.end_run()


if __name__ == '__main__':
    main()
