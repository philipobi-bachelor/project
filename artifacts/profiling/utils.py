import os
from typing import Iterable, Iterator


class Col:
    borderLeft = 0b10
    borderRight = 0b01

    def __init__(
        self,
        name: str,
        rows: Iterable[str],
        colType: str,
        borders: int | None = None,
    ):
        self.name = name
        self.rows = iter(rows)
        self.colType = colType
        self.borders = borders if borders is not None else 0b00

    def __iter__(self):
        return self

    def __next__(self):
        return next(self.rows)


class Table:
    defs = []

    def __init__(
        self,
        *cols: Col,
        rowLines: bool = False,
        colLines: bool = False,
    ):
        self.cols = cols
        self.rowLines = rowLines
        self.colLines = colLines

    def lines(self) -> Iterator[str]:
        preamble = ""
        if not self.colLines:
            for colLeft, colRight in zip(self.cols[:-1], self.cols[1:]):
                sep = (
                    " | "
                    if (
                        colLeft.borders & Col.borderRight
                        | colRight.borders & Col.borderLeft
                    )
                    else " "
                )
                preamble += sep + colRight.colType
            firstCol = self.cols[0]
            lastCol = self.cols[-1]
            preamble = (
                ("| " if firstCol.borders & Col.borderLeft else "")
                + firstCol.colType
                + preamble
                + ("|" if lastCol.borders & Col.borderRight else "")
            )
        else:
            preamble = "| " + " | ".join((col.colType for col in self.cols)) + " |"

        linesep = r" \\\hline" if self.rowLines else r" \\"
        yield "{"
        yield from Table.defs
        yield r"\begin{tabular}{" + preamble + "}"
        yield " & ".join((col.name for col in self.cols)) + linesep
        for rowCells in zip(*self.cols):
            yield " & ".join(rowCells) + linesep
        yield r"\end{tabular}"
        yield "}"

    def render(self) -> str:
        return "\n".join(self.lines())


def readlinesReversed(path, bufsiz=8192):
    # based on https://stackoverflow.com/a/23646049
    with open(path, "rb") as f:
        pos = f.seek(0, os.SEEK_END)
        segment = None
        while pos > 0:
            pos_new = f.seek(max(pos - bufsiz, 0))
            buf = f.read(pos - pos_new)
            lines = buf.split("\n".encode())
            if segment is not None:
                lines[-1] += segment
            segment = lines[0]
            yield from map(lambda l: l.decode(), reversed(lines[1:]))
            pos = pos_new
        if segment is not None:
            yield segment.decode()
