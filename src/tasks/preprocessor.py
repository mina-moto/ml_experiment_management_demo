from typing import Tuple

import pandas as pd

from tasks.run_task import RunTask


class Preprocessor(RunTask):
    def build_input_output_path_dicts(self) -> Tuple[dict, dict]:
        input_paths_dict = {
            "train": f"{self.path_config['input']}train.csv",
            "test": f"{self.path_config['input']}test.csv",
        }
        output_paths_dict = {
            "train": f"{self.path_config['preprocessor']}train.csv",
            "test": f"{self.path_config['preprocessor']}test.csv",
        }
        return input_paths_dict, output_paths_dict

    def run(self):
        train = pd.read_csv(self.input_paths_dict["train"])
        test = pd.read_csv(self.input_paths_dict["test"])
        train = train[self.config["train_columns"]]
        test = test[self.config["test_columns"]]
        train.to_csv(self.output_paths_dict["train"], index=False)
        test.to_csv(self.output_paths_dict["test"], index=False)
