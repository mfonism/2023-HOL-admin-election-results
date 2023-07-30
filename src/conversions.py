LOOKUP = {
    "1st choice": 1,
    "2nd choice": 2,
    "3rd choice": 3,
    "4th choice": 4,
    "5th choice": 5,
}


def lookup_rank(rank: str) -> int:
    # should never get an invalid rank
    # so, watch out for your inputs
    return LOOKUP[rank]
