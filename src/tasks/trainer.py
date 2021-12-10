import pickle
from typing import Tuple

import mlflow.sklearn
import pandas as pd
from luigi.util import requires
from sklearn import linear_model

from tasks.preprocessor import Preprocessor
from tasks.run_task import RunTask


@requires(Preprocessor)
class Trainer(RunTask):
    def build_input_output_path_dicts(self) -> Tuple[dict, dict]:
        input_paths_dict = {
            "train": f"{self.path_config['Preprocessor']}train.csv",
            "test": f"{self.path_config['Preprocessor']}test.csv",
        }
        output_paths_dict = {
            "model": f"{self.path_config['Trainer']}model",
        }
        return input_paths_dict, output_paths_dict

    def run(self):
        train = pd.read_csv(
            self.input_paths_dict["train"],
            index_col='PassengerId')
        X = train.drop("Survived", axis=1)
        y = train["Survived"]
        mlflow.sklearn.autolog()
        reg = linear_model.RidgeClassifier(random_state=self.config["seed"])
        reg.fit(X, y)
        pickle.dump(reg, open(self.output_paths_dict["model"], "wb"))
