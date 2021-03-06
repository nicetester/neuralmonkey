from typing import List, Iterable, Callable
import gzip
import csv
import io

from neuralmonkey.logging import warn


def get_plain_text_reader(encoding: str = "utf-8") -> Callable[[List[str]],
                                                               Iterable
                                                               [List[str]]]:
    """Get reader for space-separated tokenized text."""
    def reader(files: List[str]) -> Iterable[List[str]]:
        for path in files:

            if path.endswith(".gz"):
                with gzip.open(path, 'r') as f_data:
                    for line in f_data:
                        yield str(line, 'utf-8').strip().split(" ")
            else:
                with open(path, encoding=encoding) as f_data:
                    for line in f_data:
                        yield line.strip().split(" ")

    return reader


def column_separated_reader(column: int, delimiter: str = "\t",
                            quotechar: str = None,
                            encoding: str = "utf-8") -> Callable[[List[str]],
                                                                 Iterable
                                                                 [List[str]]]:
    """Get reader for delimiter-separated tokenized text.

    Args:
        column: number of column to be returned. It starts with 1 for the first
    """
    def reader(files: List[str]) -> Iterable[List[str]]:
        text_reader = get_plain_text_reader(encoding)
        for line in text_reader(files):
            io_line = io.StringIO(' '.join(line))
            parsed_csv = list(csv.reader(io_line, delimiter=delimiter,
                                         quotechar=quotechar,
                                         skipinitialspace=True))
            if len(parsed_csv[0]) < column:
                warn("There is a missing column number {} in the dataset."
                     .format(column))
                yield []

            yield parsed_csv[0][column - 1].split(' ')

    return reader


def csv_reader(column: int):
    return column_separated_reader(column=column, delimiter=',', quotechar='"')


def tsv_reader(column: int):
    return column_separated_reader(column=column, delimiter='\t',
                                   quotechar=None)


# pylint: disable=invalid-name
UtfPlainTextReader = get_plain_text_reader()
# pylint: enable=invalid-name
