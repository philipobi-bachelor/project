import re

if __name__ == "__main__":
    with (
        open("basf2-loc", "r") as f,
        open("basf2-loc.csv", "w") as fout,
    ):
        for line in f.readlines():
            if line[0] == "-":
                continue
            cols = re.split(r"\s{2,}", line)
            fout.write(",".join(cols))
