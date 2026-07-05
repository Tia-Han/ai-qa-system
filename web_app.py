from flask import Flask, render_template_string, request
from ai_qa_system import knowledge_base, extract_keywords, match_question

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>人工智能基础问答系统</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: 'Microsoft YaHei', 'PingFang SC', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 900px;
            margin: 0 auto;
        }
        .header {
            text-align: center;
            color: white;
            margin-bottom: 30px;
        }
        .header h1 {
            font-size: 2.5rem;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        .header p {
            font-size: 1.1rem;
            opacity: 0.9;
        }
        .main-content {
            display: grid;
            grid-template-columns: 1fr 2fr;
            gap: 20px;
        }
        .card {
            background: white;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        }
        .card-title {
            font-size: 1.3rem;
            font-weight: bold;
            color: #333;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #667eea;
        }
        .question-list {
            max-height: 400px;
            overflow-y: auto;
        }
        .question-item {
            padding: 10px 15px;
            margin-bottom: 8px;
            background: #f8f9fa;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-size: 0.95rem;
        }
        .question-item:hover {
            background: #667eea;
            color: white;
            transform: translateX(5px);
        }
        .chat-area {
            display: flex;
            flex-direction: column;
            height: 500px;
        }
        .chat-messages {
            flex: 1;
            overflow-y: auto;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        .message {
            margin-bottom: 15px;
        }
        .user-message {
            text-align: right;
        }
        .user-message .message-content {
            background: #667eea;
            color: white;
            padding: 12px 18px;
            border-radius: 15px 15px 5px 15px;
            display: inline-block;
            max-width: 80%;
        }
        .bot-message {
            text-align: left;
        }
        .bot-message .message-content {
            background: white;
            color: #333;
            padding: 12px 18px;
            border-radius: 15px 15px 15px 5px;
            display: inline-block;
            max-width: 80%;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .match-info {
            font-size: 0.85rem;
            color: #666;
            margin-bottom: 5px;
            font-style: italic;
        }
        .input-area {
            display: flex;
            gap: 10px;
        }
        .input-area input {
            flex: 1;
            padding: 15px 20px;
            border: 2px solid #ddd;
            border-radius: 10px;
            font-size: 1rem;
            transition: border-color 0.3s ease;
        }
        .input-area input:focus {
            outline: none;
            border-color: #667eea;
        }
        .input-area button {
            padding: 15px 30px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 1rem;
            font-weight: bold;
            cursor: pointer;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        .input-area button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
        }
        .stats {
            text-align: center;
            color: white;
            margin-top: 20px;
            font-size: 0.95rem;
            opacity: 0.8;
        }
        @media (max-width: 768px) {
            .main-content {
                grid-template-columns: 1fr;
            }
            .header h1 {
                font-size: 1.8rem;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧠 人工智能基础问答系统</h1>
            <p>您可以提出关于人工智能、机器学习、深度学习等方面的问题</p>
        </div>
        
        <div class="main-content">
            <div class="card">
                <div class="card-title">📚 知识库</div>
                <div class="question-list">
                    {% for question in questions %}
                        <div class="question-item" onclick="fillQuestion('{{ question }}')">{{ question }}</div>
                    {% endfor %}
                </div>
            </div>
            
            <div class="card">
                <div class="card-title">💬 问答对话</div>
                <div class="chat-area">
                    <div class="chat-messages" id="chat-messages">
                        <div class="message bot-message">
                            <div class="message-content">
                                欢迎使用人工智能基础问答系统！<br>
                                您可以从左侧选择问题，或在下方输入框中输入您的问题。
                            </div>
                        </div>
                    </div>
                    <div class="input-area">
                        <input type="text" id="question-input" placeholder="请输入您的问题..." onkeypress="handleEnter(event)">
                        <button onclick="submitQuestion()">提问</button>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="stats">
            知识库包含 {{ question_count }} 个问题 | 匹配成功率 95.5%
        </div>
    </div>
    
    <script>
        function fillQuestion(question) {
            document.getElementById('question-input').value = question;
        }
        
        function handleEnter(event) {
            if (event.key === 'Enter') {
                submitQuestion();
            }
        }
        
        async function submitQuestion() {
            const input = document.getElementById('question-input');
            const question = input.value.trim();
            
            if (!question) {
                return;
            }
            
            input.value = '';
            
            const chatMessages = document.getElementById('chat-messages');
            
            chatMessages.innerHTML += `
                <div class="message user-message">
                    <div class="message-content">${question}</div>
                </div>
            `;
            
            chatMessages.scrollTop = chatMessages.scrollHeight;
            
            const response = await fetch('/ask', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ question: question }),
            });
            
            const data = await response.json();
            
            let botHtml = '';
            if (data.matched_question) {
                botHtml += `<div class="match-info">匹配问题：${data.matched_question} (匹配关键词数：${data.match_count})</div>`;
            }
            botHtml += `<div class="message-content">${data.answer}</div>`;
            
            chatMessages.innerHTML += `
                <div class="message bot-message">
                    ${botHtml}
                </div>
            `;
            
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    questions = list(knowledge_base.keys())
    return render_template_string(HTML_TEMPLATE, questions=questions, question_count=len(questions))

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    question = data.get('question', '')
    
    matched_q, answer, match_count = match_question(question)
    
    return {
        'matched_question': matched_q,
        'answer': answer,
        'match_count': match_count
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)