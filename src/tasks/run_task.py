import os
from abc import abstractmethod
from typing import Tuple

import luigi
import mlflow
from luigi.configuration import get_config


class RunTask(luigi.Task):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = get_config(
            os.getenv("LUIGI_CONFIG_PARSER")
        )[self.__class__.__name__]

        experiment_id = mlflow.active_run().info.experiment_id
        run_id = mlflow.active_run().info.run_id

        self.path_config = get_config(
            os.getenv("LUIGI_CONFIG_PARSER"))["PathConfig"]
        self.artifacts_uri_path = f"./mlruns/{experiment_id}/{run_id}/artifacts/"

        # タスクごとにPathConfigが指定されていなければデフォルト値設定
        # デフォルトパス ./mlruns/{experiment_id}/{run_id}/artifacts/{task_name}/
        for task_name in ["preprocessor", "trainer", "prediction"]:
            self.path_config.setdefault(
                task_name,
                f"{self.artifacts_uri_path}{task_name}/")
        # 入出力パス output_paths_dictのvaluesのパスにファイルが既にある場合、そのタスクは行われない
        self.input_paths_dict, self.output_paths_dict = self.build_input_output_path_dicts()
        for output_path in self.output_paths_dict.values():
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

    @abstractmethod
    def build_input_output_path_dicts(self) -> Tuple[dict, dict]:
        """
        クラスの入出力パスをそれぞれdictで返す

        Returns:
            input_paths_dict,output_paths_dict
        """
        pass

    def output(self):
        return list(map(lambda x: luigi.LocalTarget(x),
                        self.output_paths_dict.values()))