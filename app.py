import requests
import json
from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

# 初始化数据库
def init_db():
    conn = sqlite3.connect('chat_history.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_message TEXT NOT NULL,
            bot_response TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

init_db()

api_key = 'sk-'  
endpoint = 'https://api.deepseek.com/chat/completions'  

def call_deepseek_api(question):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }
    data = {
        "model": "deepseek-chat", 
        "messages": [
            {"role": "system", "content": "你是一袋猫粮."},
            {"role": "user", "content": question}
        ],
        "stream": False
    }

    try:
        response = requests.post(endpoint, headers=headers, json=data)
        response.raise_for_status()
        bot_response = response.json()['choices'][0]['message']['content']
        print(f"API 响应: {bot_response}")  
        return bot_response
    except requests.exceptions.RequestException as e:
        print(f"API 调用失败: {str(e)}")  
        raise

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    print("收到请求")  
    user_message = request.json.get('message')
    if not user_message:
        print("未提供消息")  
        return jsonify({'error': 'No message provided'}), 400

    print(f"用户输入: {user_message}")  

    try:
        bot_response = call_deepseek_api(user_message)
        print(f"Bot response: {bot_response}")  
        save_chat_history(user_message, bot_response)
        return jsonify({'response': bot_response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def save_chat_history(user_message, bot_response):
    conn = sqlite3.connect('chat_history.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO chat_history (user_message, bot_response)
        VALUES (?, ?)
    ''', (user_message, bot_response))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    app.run(debug=True)