import os

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