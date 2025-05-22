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


def extract(path):
    events = []
    event = None
    fitAndStore = None
    for line in filter(
        lambda line: "NewV0Fitter::" in line or "V0FinderModule::" in line,
        readlines_reversed(path),
    ):

        [_, method, *params] = line.split()

        match method:
            case "V0FinderModule::event":
                if event is not None:
                    events.append(event)
                
                [t_str, *_] = params
                event = {"t": float(t_str), "fitAndStore": []}

            case "NewV0Fitter::fitAndStore":
                if fitAndStore is not None:
                    event["fitAndStore"].append(fitAndStore)
                
                [_, ptype, t_str, *_] = params
                fitAndStore = {
                    "t": float(t_str),
                    "ptype": ptype[:-1],
                    "vertexFit": [],
                    "fitGFRaveVertex": [],
                    "removeHitsAndRefit": [],
                }

            case "NewV0Fitter::vertexFit":
                [t_str, *_] = params
                fitAndStore["vertexFit"].append(float(t_str))

            case "NewV0Fitter::fitGFRaveVertex":
                [t_str, *_] = params
                fitAndStore["fitGFRaveVertex"].append(float(t_str))

            case "NewV0Fitter::removeHitsAndRefit":
                [t_str, *_] = params
                fitAndStore["removeHitsAndRefit"].append(float(t_str))
    
    return events

def main():
    events = extract("v0ValidationGenerateSample.py.log")
    pprint(events[:10])

main()