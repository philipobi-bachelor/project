import pandas as pd

if __name__ == "__main__":

    [df] = pd.read_html("livebench.html")

    df.sort_values(
        "Coding Average",
        ascending=False,
    ).to_csv(
        "livebench-coding.csv",
        index=False,
        float_format="%.2f",
    )

    [df] = pd.read_html("lmarena.html")

    df.sort_values("Coding").to_csv(
        "lmarena-coding.csv",
        index=False,
    )
