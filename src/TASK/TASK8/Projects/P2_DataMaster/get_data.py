from sklearn.datasets import load_iris
import pandas as pd

data = pd.DataFrame(load_iris().data)
print(data)
data.to_csv(r'./iris.csv', index=False)