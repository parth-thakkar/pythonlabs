import numpy as np
import pandas as pd

# ndarray
arr = np.array([[1, 2], [3, 4]])
#print(arr[0, 1])  # 2
print(arr)
# DataFrame
df = pd.DataFrame({'A': [1, 3], 'B': [2, 4]})
print(df['B'][0])  # 2
print(df)