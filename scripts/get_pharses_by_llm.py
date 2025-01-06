import json
from time import sleep
from groq import Groq

def try_get_latin_phrases(api_key):
    # 创建 Groq 客户端实例
    client = Groq(api_key=api_key)
    
    # 发送请求以生成拉丁词组
    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {
                "role": "system",
                "content": "{\n  \"task\": \"Upon receiving the command 'next', generate five Latin phrases that are not commonly used in modern English. Each phrase should be unique and not have a direct equivalent in contemporary English. Provide each phrase along with its meaning in English. The phrases should be presented in a JSON object with a 'phrases' key containing an array of objects, each with 'latin' and 'english_meaning' keys.\",\n  \"output_format\": {\n    \"phrases\": [\n      {\n        \"latin\": \"String\",\n        \"english_meaning\": \"String\"\n      },\n      {\n        \"latin\": \"String\",\n        \"english_meaning\": \"String\"\n      },\n      {\n        \"latin\": \"String\",\n        \"english_meaning\": \"String\"\n      },\n      {\n        \"latin\": \"String\",\n        \"english_meaning\": \"String\"\n      },\n      {\n        \"latin\": \"String\",\n        \"english_meaning\": \"String\"\n      }\n    ]\n  },\n  \"trigger\": \"next\"\n}"
            },
            {
                "role": "user",
                "content": "next"
            },
        ],
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=False,
        response_format={"type": "json_object"},
        stop=None,
    )
    
    # 获取生成的 JSON 字符串
    generated_json_str = completion.choices[0].message.content
    
    # 解析 JSON 字符串为 Python 对象
    generated_json = json.loads(generated_json_str)
    
    # 返回生成的拉丁词组数组
    return generated_json['phrases']

def get_latin_phrases(api_key):
    while True:
        try:
            return  try_get_latin_phrases(api_key)
        except:
            sleep(4)