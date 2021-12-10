import pickle
from typing import Tuple

import pandas as pd
from luigi.util import requires

from tasks.preprocessor import Preprocessor
from tasks.run_task import RunTask
from tasks.trainer import Trainer


@requires(Preprocessor, Trainer)
class Prediction(RunTask):
    def build_input_output_path_dicts(self) -> Tuple[dict, dict]:
        input_paths_dict = {
            "test": f"{self.path_config['Preprocessor']}test.csv",
            "model": f"{self.path_config['Trainer']}model",
        }
        output_paths_dict = {
            "test_prediction": f"{self.path_config['Prediction']}test_prediction.csv", }
        return input_paths_dict, output_paths_dict

    def run(self):
        test = pd.read_csv(
            self.input_paths_dict["test"],
            index_col="PassengerId")
        model = pickle.load(open(self.input_paths_dict["model"], "rb"))
        test_prediction = pd.DataFrame(
            model.predict(test),
            columns=["Survived"],
            index=test.index
        )
        test_prediction.to_csv(self.output_paths_dict["test_prediction"])
