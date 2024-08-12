import requests
import json

api_key = 'sk-'  
endpoint = 'https://api.deepseek.com/chat/completions'  # 确保这是正确的API端点

def test_api_key():
    question = '你好，我饿了'  
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }
    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": question}
        ],
        "stream": False
    }

    print(f'请求URL: {endpoint}')
    print(f'请求头: {headers}')
    print(f'请求数据: {json.dumps(data, indent=4)}')

    try:
        response = requests.post(endpoint, headers=headers, json=data)
        response.raise_for_status()  

        print('API响应成功，状态码:', response.status_code)
        print('响应内容:', response.json())
    except requests.exceptions.RequestException as e:
        print('API测试失败')
        print('错误信息:', str(e))
        if response is not None:
            print('响应状态码:', response.status_code)
            print('响应内容:', response.text)

if __name__ == '__main__':
    test_api_key()

