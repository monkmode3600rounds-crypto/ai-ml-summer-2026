import pandas as pd

data = {'name': ['Alice', 'Bob'], 'age': [25, 30]}
df = pd.DataFrame(data)

# 這行會觸發 KeyError
print(df['wrong_column'])