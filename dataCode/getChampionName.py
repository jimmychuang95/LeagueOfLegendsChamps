import pandas as pd

# 读取 CSV 文件
csv_file = './data/champions/all.csv'  # 替换为您的 CSV 文件路径
df = pd.read_csv(csv_file)

# 检查 DataFrame 是否有足够的列
if df.shape[1] >= 2:
    # 提取第二列（假设列的索引从 0 开始）
    column_values = df.iloc[:, 2].tolist()

    # 删除重复的值
    unique_values = list(set(column_values))
else:
    print("CSV 文件的列数不足以提取第二列")
    unique_values = []

# unique_values 现在包含第二列的唯一值
print(unique_values)
print(len(unique_values))