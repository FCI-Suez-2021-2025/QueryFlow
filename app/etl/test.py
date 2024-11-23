import pandas as pd
from tabulate import tabulate

df = pd.DataFrame({"calories": [420, 380, 390], "duration": [50, 40, 45]})
print(tabulate(df, headers=df.keys()))
