import pandas as pd

df = pd.read_excel("C:/Users/81317/OneDrive/桌面/Contenir.xlsx", header=0, index_col=0)

# 准备一个空的DataFrame来存储转换后的数据
new_df = pd.DataFrame(columns=['CodeA', 'CodeM', 'qteM'])

# 处理数据
for index, row in df.iterrows():
    for i, value in enumerate(row):
        formatted_data = {'CodeA': index, 'CodeM': i + 1, 'qteM': value}
        new_df = new_df.append(formatted_data, ignore_index=True)

# 保存为CSV文件
output_file_path = 'C:/Users/81317/OneDrive/桌面/Contenir.csv'  # 您希望保存CSV文件的路径
new_df.to_csv(output_file_path, index=False)
