import csv
import unicodedata

def remove_diacritics(text):
    """去除变音符号"""
    return ''.join(c for c in unicodedata.normalize('NFKD', text) 
                  if not unicodedata.combining(c))

def process_column(csv_file, column_name):
    """处理CSV文件指定列"""
    processed_data = []
    
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file,delimiter=" ")
        for row in reader:
            # 去除变音符号
            text = remove_diacritics(row[column_name])
            # 去除包含"-"或"."的整个词
            words = [word for word in text.split() if '-' not in word and '.' not in word]
            processed_data.append(text)
    
    return processed_data

def save_processed_data(data, output_file):
    """保存处理后的数据"""
    with open(output_file, 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Processed Data'])  # 写入表头
        for item in data:
            writer.writerow([item])

if __name__ == "__main__":
    # 示例用法
    input_csv = 'latin_phrases.csv'  # 输入CSV文件
    output_csv = 'processed_data.csv'  # 输出文件
    column_to_process = 'latin'  # 要处理的列名
    
    # 处理数据
    processed_data = process_column(input_csv, column_to_process)
    
    # 保存结果
    save_processed_data(processed_data, output_csv)
    print(f"处理完成，结果已保存到 {output_csv}")
