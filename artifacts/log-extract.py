import os
from pprint import pprint

def readlines_reversed(path, bufsiz=8192):
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


def extract(filepath, dbpath):
    import sqlite3
    con = sqlite3.connect(dbpath)
    event = None
    fitAndStore = None
    vertexFit = None

    with con:
        cur = con.cursor()

        for line in filter(
            lambda line: "NewV0Fitter::" in line or "V0FinderModule::" in line,
            readlines_reversed(filepath),
        ):

            [_, method, *params] = line.split()

            match method:
                case "V0FinderModule::event":
                    # [INFO] V0FinderModule::event 139.483 ms
                    [t_str, *_] = params
                    
                    cur.execute("INSERT INTO event (duration) VALUES (?)", (float(t_str),))
                    event = cur.lastrowid

                case "NewV0Fitter::fitAndStore":
                    # [INFO] NewV0Fitter::fitAndStore <type: gamma> 3.387 ms
                    [_, ptype, t_str, *_] = params
                    ptype = ptype[:-1]
                    
                    cur.execute(
                        "INSERT INTO fitAndStore (ptype, duration, event) VALUES (?, ?, ?)",
                        (ptype, float(t_str), event)
                        )
                    fitAndStore = cur.lastrowid
                
                case "NewV0Fitter::vertexFit":
                    [t_str, *_] = params
                    
                    cur.execute(
                        "INSERT INTO vertexFit (duration, fitAndStore) VALUES (?, ?)",
                        (float(t_str), fitAndStore)
                    )
                    vertexFit = cur.lastrowid

                case "NewV0Fitter::fitGFRaveVertex":
                    [t_str, *_] = params
                    
                    cur.execute(
                        "INSERT INTO fitGFRaveVertex (duration, vertexFit) VALUES (?, ?)",
                        (float(t_str), vertexFit)
                    )

                case "NewV0Fitter::removeHitsAndRefit":
                    [t_str, *_] = params
                    
                    cur.execute(
                        "INSERT INTO removeHitsAndRefit (duration, fitAndStore) VALUES (?, ?)",
                        (float(t_str), fitAndStore)
                    )

def main():
    extract("v0finder-validation.log", "v0finder-profiling.sqlite")

main()