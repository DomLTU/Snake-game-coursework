import json
import os


class ScoreManager:
    """
    Singleton Pattern: Ensures only one instance manages the high score.
    File I/O: Handles reading and writing the score to a JSON file in cache.
    """
    _instance = None
    _file_path = os.path.join(os.path.dirname(__file__), "..", "resources", "cache", "highscore.json")

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ScoreManager, cls).__new__(cls)
            cls._instance._load_score()
        return cls._instance

    def _load_score(self):
        self.__high_score = 0
        if os.path.exists(self._file_path):
            try:
                with open(self._file_path, "r") as f:
                    data = json.load(f)
                    self.__high_score = data.get("high_score", 0)
            except (json.JSONDecodeError, IOError):
                pass

    def _save_score(self):
        with open(self._file_path, "w") as f:
            json.dump({"high_score": self.__high_score}, f)

    @property
    def high_score(self):
        return self.__high_score

    @high_score.setter
    def high_score(self, value):
        if value > self.__high_score:
            self.__high_score = value
            self._save_score()
