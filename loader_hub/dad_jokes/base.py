"""dad_jokes reader"""

import requests
from typing import List

from llama_index.readers.base import BaseReader
from llama_index.readers.schema.base import Document

class DadJokesReader(BaseReader):
    """Dad jokes reader.

    Reads a random dad joke.

    """

    def _get_random_dad_joke(self):
        response = requests.get("https://icanhazdadjoke.com/", headers={"Accept": "application/json"})
        response.raise_for_status()
        json_data = response.json()
        return json_data["joke"]

    def load_data(self) -> List[Document]:
        """Return a random dad joke.

        Args:
            None.

        """
        return [Document(self._get_random_dad_joke())]