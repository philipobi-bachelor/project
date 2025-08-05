import pandas as pd

if __name__ == "__main__":
    [df] = pd.read_html("lmarena.html")

    df.sort_values("Coding").to_csv(
        "lmarena-coding.csv",
        index=False,
    )
