import pandas as pd
from ml import inference
import argparse

def main():
    arg = argparse.ArgumentParser()
    arg.add_argument("-i", "--input", type = str, default = "../data/train.csv")
    arg.add_argument("-o", "--output", type = str, default = "predictions.csv")
    args = arg.parse_args()
    params = vars(args)

    df = pd.read_csv(params["input"]).drop(["Artist Name", "Track Name", "Class"],axis = 1)
    y_pr = inference(df)
    df_pr = pd.DataFrame(y_pr, index= df.index, columns = ["Class"])
    df_pr.to_csv(params["output"])

if __name__=="__main__":
    main()