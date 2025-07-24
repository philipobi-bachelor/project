import pandas as pd
if __name__ == "__main__":

    [df] = pd.read_html("livebench.html")

    df.sort_values(
        "Coding Average",
        ascending=False,
    ).to_csv(
        "livebench-coding.csv",
        index=False,
    )


    df.sort_values(
        "Agentic Coding Average",
        ascending=False,
    ).to_csv(
        "livebench-agentic-coding.csv",
        index=False,
    )
