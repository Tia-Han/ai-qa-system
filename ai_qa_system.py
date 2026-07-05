knowledge_base = {
    "什么是人工智能？": "人工智能（Artificial Intelligence，简称AI）是计算机科学的一个分支，致力于研究、开发用于模拟、延伸和扩展人的智能的理论、方法、技术及应用系统。",
    "什么是机器学习？": "机器学习（Machine Learning）是人工智能的核心技术之一，它使计算机系统能够从数据中学习并改进其性能，而无需进行明确编程。",
    "什么是深度学习？": "深度学习（Deep Learning）是机器学习的一个子集，它使用多层神经网络来模拟人脑的学习过程。",
    "人工智能和机器学习的关系？": "人工智能是一个广泛的概念，指的是机器表现出的智能。机器学习是实现人工智能的一种方法。简单来说：人工智能 > 机器学习 > 深度学习。",
    "什么是神经网络？": "神经网络（Neural Network）是一种模仿人脑神经元结构和功能的计算模型，由大量的节点和它们之间的连接组成。",
    "什么是监督学习？": "监督学习（Supervised Learning）是机器学习的一种类型，它使用带有标签的训练数据来训练模型，常见任务包括分类和回归。",
    "什么是非监督学习？": "非监督学习（Unsupervised Learning）是机器学习的一种类型，它使用不带标签的训练数据来训练模型，常见任务包括聚类和降维。",
    "什么是强化学习？": "强化学习（Reinforcement Learning）是机器学习的一种类型，它通过智能体与环境的交互来学习最优行为策略。",
    "什么是自然语言处理？": "自然语言处理（Natural Language Processing，简称NLP）是人工智能的一个分支，它使计算机能够理解、处理和生成人类语言。",
    "什么是图像识别？": "图像识别（Image Recognition）是计算机视觉的一个重要领域，它使计算机能够识别和分类图像中的物体、场景和人物。",
    "什么是数据挖掘？": "数据挖掘（Data Mining）是从大量数据中发现模式、规律和知识的过程，结合了统计学、机器学习等多种方法。",
    "什么是特征工程？": "特征工程（Feature Engineering）是机器学习中非常重要的一个环节，它包括选择、提取、转换和创建特征，以便更好地表示数据。",
    "什么是过拟合？": "过拟合（Overfitting）是指模型在训练数据上表现很好，但在测试数据上表现很差的现象，意味着模型过于复杂。",
    "什么是欠拟合？": "欠拟合（Underfitting）是指模型在训练数据和测试数据上都表现很差的现象，意味着模型过于简单。",
    "什么是梯度下降？": "梯度下降（Gradient Descent）是一种优化算法，用于最小化损失函数，通过沿梯度的反方向更新参数来逼近最优解。",
    "什么是卷积神经网络？": "卷积神经网络（Convolutional Neural Network，简称CNN）是一种专门用于处理网格数据（如图像）的深度学习模型。",
    "什么是循环神经网络？": "循环神经网络（Recurrent Neural Network，简称RNN）是一种专门用于处理序列数据的深度学习模型。",
    "什么是Transformer？": "Transformer是一种基于自注意力机制的深度学习模型，由Google在2017年提出，是BERT、GPT等大型语言模型的基础。",
    "什么是BERT？": "BERT（Bidirectional Encoder Representations from Transformers）是Google在2018年提出的一种预训练语言模型。",
    "Python在人工智能中的作用？": "Python是人工智能领域最流行的编程语言，拥有丰富的机器学习和深度学习库，如TensorFlow、PyTorch、Scikit-learn等。"
}

import re

stop_words = {'什', '么', '是', '的', '在', '中', '和', '与', '及', '等', '有', '了', '为', '以', '对', '从', '到', '用', '会', '可以', '这个', '那个', '这些', '那些'}

keyword_aliases = {
    'ai': {'人', '工', '智', '能'},
    'cnn': {'卷', '积', '神', '经', '网', '络'},
    'rnn': {'循', '环', '神', '经', '网', '络'},
    'nlp': {'语', '言', '处', '理'},
}

def extract_keywords(text):
    keywords = set()
    for char in text:
        if '\u4e00' <= char <= '\u9fa5':
            if char not in stop_words:
                keywords.add(char)
    english_words = re.findall(r'[a-zA-Z]+', text)
    for word in english_words:
        if len(word) >= 2:
            word_lower = word.lower()
            keywords.add(word_lower)
            if word_lower in keyword_aliases:
                keywords.update(keyword_aliases[word_lower])
    return keywords

keywords_to_questions = {}
for question in knowledge_base:
    keywords = extract_keywords(question)
    for keyword in keywords:
        if keyword not in keywords_to_questions:
            keywords_to_questions[keyword] = []
        keywords_to_questions[keyword].append(question)

def match_question(user_question):
    user_keywords = extract_keywords(user_question)
    
    if user_question in knowledge_base:
        return user_question, knowledge_base[user_question], len(user_keywords)
    
    candidate_questions = set()
    for keyword in user_keywords:
        if keyword in keywords_to_questions:
            candidate_questions.update(keywords_to_questions[keyword])
    
    if not candidate_questions:
        return None, "未找到答案", 0
    
    max_match_count = 0
    best_match = None
    
    for question in candidate_questions:
        question_keywords = extract_keywords(question)
        intersection = user_keywords & question_keywords
        match_count = len(intersection)
        
        if match_count > max_match_count:
            max_match_count = match_count
            best_match = question
        elif match_count == max_match_count:
            if question_keywords.issubset(user_keywords):
                best_match = question
            elif len(question_keywords) < len(extract_keywords(best_match)):
                best_match = question
    
    return best_match, knowledge_base.get(best_match, "未找到答案"), max_match_count

def main_cli():
    print("欢迎使用人工智能基础问答系统！")
    print("输入'退出'结束程序。\n")
    
    question_history = []
    
    while True:
        user_input = input("请输入您的问题：")
        if user_input == "退出":
            print("\n感谢使用！再见！")
            break
        
        question_history.append(user_input)
        
        matched_q, answer, match_count = match_question(user_input)
        print(f"\n回答：{answer}\n")
    
    print("\n提问记录：")
    for i, q in enumerate(question_history, 1):
        print(f"{i}. {q}")

if __name__ == "__main__":
    main_cli()

import tkinter as tk
from tkinter import ttk

def main_gui():
    root = tk.Tk()
    root.title("人工智能基础问答系统")
    root.geometry("800x600")
    root.resizable(True, True)
    
    style = ttk.Style()
    style.theme_use('clam')
    
    notebook = ttk.Notebook(root)
    notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    frame1 = ttk.Frame(notebook)
    notebook.add(frame1, text='问答')
    
    frame2 = ttk.Frame(notebook)
    notebook.add(frame2, text='提问记录')
    
    welcome_label = ttk.Label(frame1, text="欢迎使用人工智能基础问答系统！", font=('Arial', 14, 'bold'))
    welcome_label.pack(pady=10)
    
    question_label = ttk.Label(frame1, text="请输入您的问题：")
    question_label.pack(pady=5)
    
    question_entry = ttk.Entry(frame1, width=60, font=('Arial', 12))
    question_entry.pack(pady=5)
    
    answer_label = ttk.Label(frame1, text="回答：")
    answer_label.pack(pady=5)
    
    answer_text = tk.Text(frame1, width=70, height=15, font=('Arial', 11), wrap=tk.WORD)
    answer_text.pack(pady=5)
    answer_text.config(state=tk.DISABLED)
    
    question_history = []
    history_listbox = tk.Listbox(frame2, width=80, height=25, font=('Arial', 11))
    history_listbox.pack(pady=10)
    
    def ask_question(event=None):
        user_input = question_entry.get().strip()
        if not user_input:
            return
        
        question_history.append(user_input)
        
        matched_q, answer, match_count = match_question(user_input)
        
        answer_text.config(state=tk.NORMAL)
        answer_text.delete(1.0, tk.END)
        if matched_q:
            answer_text.insert(tk.END, f"匹配问题：{matched_q}\n\n")
        answer_text.insert(tk.END, answer)
        answer_text.config(state=tk.DISABLED)
        
        question_entry.delete(0, tk.END)
        
        history_listbox.delete(0, tk.END)
        for i, q in enumerate(question_history, 1):
            history_listbox.insert(tk.END, f"{i}. {q}")
    
    def clear_history():
        question_history.clear()
        history_listbox.delete(0, tk.END)
        answer_text.config(state=tk.NORMAL)
        answer_text.delete(1.0, tk.END)
        answer_text.config(state=tk.DISABLED)
    
    def exit_app():
        root.destroy()
    
    button_frame = ttk.Frame(frame1)
    button_frame.pack(pady=10)
    
    ask_button = ttk.Button(button_frame, text="提问", command=ask_question)
    ask_button.pack(side=tk.LEFT, padx=5)
    
    clear_button = ttk.Button(button_frame, text="清空", command=clear_history)
    clear_button.pack(side=tk.LEFT, padx=5)
    
    exit_button = ttk.Button(button_frame, text="退出", command=exit_app)
    exit_button.pack(side=tk.LEFT, padx=5)
    
    question_entry.bind('<Return>', ask_question)
    question_entry.focus()
    
    root.mainloop()

if __name__ == "__main__":
    main_gui()