import os
import pandas as pd

def merge_csv_files(input_dir, output_file):
    # 用于存储所有CSV文件数据的列表
    all_data = []

    # 遍历目录中的所有文件
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith('.csv'):
                # 构造文件路径
                file_path = os.path.join(root, file)
                
                # 提取文件名中的keyword、start_date、end_date
                file_name = os.path.splitext(file)[0]  # 去掉文件扩展名
                parts = file_name.split('-')
                if len(parts) >= 3:
                    keyword = parts[0]  # 关键词部分
                    start_date = '-'.join(parts[1:4]) # 开始日期
                    end_date ='-'.join(parts[4:7]) # 结束日期
                    timeframe = f'{start_date} {end_date}'  # 时间范围
                    
                    # 读取CSV文件到DataFrame
                    df = pd.read_csv(file_path)
                    
                    # 确保包含geoName, geoCode, 和 keyword 列
                    if 'geoName' in df.columns and 'geoCode' in df.columns:
                        for keyword_column in df.columns:
                            if keyword_column not in ['geoName', 'geoCode']:
                                # 创建包含 geoCode, value, keyword, timeframe 列的DataFrame
                                temp_df = df[['geoName', 'geoCode', keyword_column]].copy()
                                temp_df['keyword'] = keyword
                                temp_df['value'] = temp_df[keyword_column]
                                temp_df['timeframe'] = timeframe
                                
                                # 保留关键列
                                temp_df = temp_df[['geoCode', 'value', 'keyword', 'timeframe']]
                                
                                # 添加到总数据列表
                                all_data.append(temp_df)

                    else:
                        print(f"Warning: Missing expected columns in {file}, skipping.")
                else:
                    print(f"Warning: Unable to parse filename structure for {file}, skipping.")

    # 合并所有DataFrame
    if all_data:
        combined_df = pd.concat(all_data, ignore_index=True)

        # 保存合并后的DataFrame为CSV
        combined_df.to_csv(output_file, index=False,na_rep='NA')
        print(f"Data merged and saved to {output_file}")
    else:
        print("No valid data found to merge.")

# 设置输入和输出路径
input_directory = 'data/yearly/process data/'
output_file = 'data/yearly/merged_data.csv'

# 调用函数合并CSV文件
merge_csv_files(input_directory, output_file)
