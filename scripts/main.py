import random
from time import sleep
from trendspy import Trends


from get_pharses_by_llm import get_latin_phrases

def filter_phrases(phrases, rules):
    # 根据提供的规则过滤词组
    filtered_phrases = []
    for phrase in phrases:
        if all(rule(phrase) for rule in rules):
            filtered_phrases.append(phrase)
            sleep(random.randrange(1,5))  # 等待60-120秒
    return filtered_phrases

def save_phrases(phrases):
    # 保存词组到文件或数据库，确保不重复
    # 这里只是一个示例，具体实现取决于你的存储方式
    with open('./data/latin_phrases.csv', 'a') as file:
        for phrase in phrases:
            file.write(f"\"{phrase['latin']}\" \"{phrase['english_meaning']}\"\n")

def read_next_five_lines(file_path, start_line=0):
    # 初始化一个空列表来存储字典
    dict_array = []
    with open(file_path, 'r') as file:
        # 将文件指针移动到指定的起始行
        for _ in range(start_line):
            next(file, None)  # 如果到达文件末尾，next将引发StopIteration异常
        try:
            # 读取5行
            for _ in range(5):
                line = next(file).strip()  # 读取一行并去除行尾的换行符
                if line:  # 如果行不为空
                   dict_array.append({"latin": line,"english_meaning":""})  # 创建字典并添加到列表中
        except StopIteration:
            # 如果读取的行数少于5行，或者到达文件末尾，StopIteration异常会被引发
            pass
    return dict_array  # 返回字典数组


def is_hot(pharse):
    try: 
        data = tr.interest_by_region(keywords=f'"{pharse["latin"]}"', timeframe="all", inc_low_vol=True)
        # 筛选出geoName为意大利或梵蒂冈的行
        selected_rows = data[data['geoName'].isin(['Italy', 'Vatican City'])]
        # 获取整个DataFrame中value的最大值
        max_value = data[pharse["latin"]].max()
        if max_value!=100:
            return False
        # 检查筛选出的行中是否有value等于第一个值的
        if selected_rows[pharse["latin"]].eq(max_value).any():
            return True
        else:
            return False
    except:
      return False

rules = [is_hot]

# 主循环
count=315
from env import proxies
tr = Trends(request_delay=2.0,proxy=proxies)
while True:
    latin_phrases = read_next_five_lines("./data/processed_data.csv",count*5)  
    filtered_phrases = filter_phrases(latin_phrases, rules)
    print(f'{filtered_phrases} {count*5}-{count*5+4}')
    count+=1
    save_phrases(filtered_phrases)