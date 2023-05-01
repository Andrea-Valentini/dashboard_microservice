from pandas import read_csv

pathfiles = "data"

def sort_csv_data_by_timestamp(file:str) -> None:


    df = read_csv(pathfiles + "/" + file)
    df = df.sort_values(by='timestamp', ascending=True)
    sorted_filename = file.replace(".csv","") + "_sorted.csv"
    df.to_csv(pathfiles + "/" + sorted_filename, index=False)


sort_csv_data_by_timestamp("prices.csv")
sort_csv_data_by_timestamp("dataset 2.csv")