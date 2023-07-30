import pathlib
from typing import Callable

import openpyxl

from . import typing as t

BASE_DIR = pathlib.Path(__file__).resolve().parent
DATA_DIR = BASE_DIR.parent / "election_data"


class Extractor:
    def __init__(
        self,
        *,
        candidates: set[str],
        data_filename: str,
        parse_rank: Callable[[str], int] = None
    ):
        self.candidates: set[t.Candidate] = candidates
        self.data_filepath: pathlib.Path = DATA_DIR / data_filename

        self.parse_rank: Callable[[str], int]
        if parse_rank is not None:
            self.parse_rank = parse_rank
        else:
            self.parse_rank = lambda rank_string: int(rank_string[0])

        self.votes: t.Vote = None

    def extract_votes(self) -> list[t.Vote]:
        if self.votes is None:
            workbook = openpyxl.load_workbook(
                filename=self.data_filepath, read_only=True
            )
            worksheet = workbook.active
            irows = worksheet.iter_rows(values_only=True)
            header_row = next(irows)
            # note that subsequent rows generated/iterated from `irows` are data rows

            # get the number of the respective columns where each candidate's ranking is recorded
            self._candidate_indexes: dict[int, t.Candidate] = {
                col_num: col_data
                for (col_num, col_data) in enumerate(header_row)
                if col_data in self.candidates
            }

            # extract the votes from each column
            self.votes: list[t.Vote] = list(
                {
                    self._candidate_indexes[col_num]: self.parse_rank(col_data)
                    for (col_num, col_data) in enumerate(data_row)
                    if col_num in self._candidate_indexes
                }
                for data_row in irows
            )

        return self.votes
