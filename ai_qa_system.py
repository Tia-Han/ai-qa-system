import re

knowledge_base = {
    "什么是人工智能？": "人工智能（Artificial Intelligence，简称AI）是计算机科学的一个分支，致力于研究、开发用于模拟、延伸和扩展人的智能的理论、方法、技术及应用系统。它使计算机能够执行通常需要人类智能才能完成的任务。",
    "什么是机器学习？": "机器学习（Machine Learning）是人工智能的核心技术之一，它使计算机系统能够从数据中学习和改进，而无需进行明确编程。机器学习算法通过分析数据模式，自动优化性能。",
    "什么是深度学习？": "深度学习（Deep Learning）是机器学习的一个子领域，使用多层神经网络来模拟人脑的学习过程。它能够自动从原始数据中提取特征，在图像识别、自然语言处理等领域取得了突破性进展。",
    "机器学习和深度学习的区别是什么？": "机器学习是人工智能的一个子集，而深度学习是机器学习的一个子集。机器学习通常需要人工提取特征，而深度学习能够自动学习特征。深度学习模型通常更深更复杂，需要更多的数据和计算资源。",
    "Python在人工智能中的作用是什么？": "Python是人工智能领域最流行的编程语言，因为它语法简洁、易于学习，拥有丰富的科学计算库（如NumPy、Pandas）和机器学习框架（如TensorFlow、PyTorch、Scikit-learn），为AI开发提供了强大的工具支持。",
    "什么是神经网络？": "神经网络（Neural Network）是一种模仿人脑神经元结构的计算模型，由大量相互连接的节点（神经元）组成。它通过调整节点之间的连接权重来学习数据模式，是深度学习的基础。",
    "什么是监督学习？": "监督学习（Supervised Learning）是机器学习的一种范式，使用带有标签的数据进行训练。模型从已知输入和输出的配对数据中学习映射关系，常用于分类和回归任务。",
    "什么是非监督学习？": "非监督学习（Unsupervised Learning）是机器学习的一种范式，使用没有标签的数据进行训练。模型从数据中自动发现隐藏的模式和结构，常用于聚类和降维任务。",
    "什么是强化学习？": "强化学习（Reinforcement Learning）是机器学习的一种范式，智能体通过与环境交互，根据获得的奖励或惩罚来学习最优行为策略。它常用于游戏AI、机器人控制等领域。",
    "什么是自然语言处理？": "自然语言处理（Natural Language Processing，简称NLP）是人工智能的一个分支，致力于使计算机能够理解、处理和生成人类语言。它涉及文本分析、机器翻译、语音识别等技术。",
    "什么是图像识别？": "图像识别（Image Recognition）是计算机视觉的核心任务，指计算机系统能够识别图像中的物体、场景和特征。它在自动驾驶、安防监控、医疗诊断等领域有广泛应用。",
    "什么是数据挖掘？": "数据挖掘（Data Mining）是从大量数据中提取有用信息和知识的过程。它结合了机器学习、统计学和数据库技术，用于发现数据中的模式、关联和异常。",
    "什么是特征工程？": "特征工程（Feature Engineering）是机器学习中重要的预处理步骤，指从原始数据中提取和选择最有价值的特征，以提高模型的性能。好的特征工程往往比选择复杂模型更重要。",
    "什么是过拟合？": "过拟合（Overfitting）是机器学习中的常见问题，指模型在训练数据上表现很好，但在测试数据上表现很差。这通常是因为模型过于复杂，学习了训练数据中的噪声而不是真正的模式。",
    "什么是欠拟合？": "欠拟合（Underfitting）是机器学习中的常见问题，指模型在训练数据和测试数据上表现都很差。这通常是因为模型过于简单，无法捕捉数据中的复杂模式。",
    "什么是梯度下降？": "梯度下降（Gradient Descent）是机器学习中常用的优化算法，用于最小化损失函数。它通过计算损失函数的梯度，沿梯度反方向更新模型参数，逐步找到最优解。",
    "什么是卷积神经网络？": "卷积神经网络（Convolutional Neural Network，简称CNN）是一种专门用于处理网格状数据（如图像）的神经网络。它使用卷积操作来提取局部特征，在图像识别任务中表现出色。",
    "什么是循环神经网络？": "循环神经网络（Recurrent Neural Network，简称RNN）是一种具有记忆能力的神经网络，能够处理序列数据。它通过循环连接保留之前的信息，常用于自然语言处理和时间序列预测。",
    "什么是Transformer？": "Transformer是一种基于自注意力机制的神经网络架构，由Google在2017年提出。它在处理序列数据时能够同时考虑所有位置的信息，是BERT、GPT等大型语言模型的基础。",
    "人工智能有哪些应用领域？": "人工智能的应用领域非常广泛，包括但不限于：自动驾驶、智能语音助手、医疗诊断、金融风控、推荐系统、智能制造、教育辅助、安防监控、智能家居等。"
}

def extract_keywords(text):
    stop_words = {'什', '么', '是', '的', '在', '中', '和', '与', '有', '哪', '些', '如', '何', '为', '么', '怎', '样', '吗', '呢', '吧', '啊', '哦', '了', '着', '过', '也', '还', '都', '就', '才', '要', '会', '可', '以', '应', '该', '很', '常', '特', '别', '比', '较', '更', '加', '最', '不', '没', '有', '一', '个', '些', '这', '种', '那', '种', '个', '那', '些', '区', '别', '作', '用', '定', '义', '领', '域', '场', '景', '解', '决', '了', '解'}
    keywords = set()
    for char in text:
        if '\u4e00' <= char <= '\u9fa5':
            if char not in stop_words:
                keywords.add(char)
    english_words = re.findall(r'[a-zA-Z]+', text)
    for word in english_words:
        if len(word) >= 2:
            keywords.add(word.lower())
    return keywords

keywords_set = set()
keywords_to_questions = {}

for question in knowledge_base.keys():
    question_keywords = extract_keywords(question)
    keywords_set.update(question_keywords)
    for keyword in question_keywords:
        if keyword not in keywords_to_questions:
            keywords_to_questions[keyword] = []
        keywords_to_questions[keyword].append(question)

def match_question(user_question):
    user_keywords = extract_keywords(user_question)
    
    if not user_keywords:
        return None, "抱歉，未找到相关答案，请尝试其他问题", 0
    
    candidate_questions = set()
    for keyword in user_keywords:
        if keyword in keywords_to_questions:
            candidate_questions.update(keywords_to_questions[keyword])
    
    if not candidate_questions:
        return None, "抱歉，未找到相关答案，请尝试其他问题", 0
    
    max_match_count = 0
    best_match = None
    
    for question in candidate_questions:
        question_keywords = extract_keywords(question)
        intersection = user_keywords & question_keywords
        match_count = len(intersection)
        
        if match_count > max_match_count:
            max_match_count = match_count
            best_match = question
        elif match_count == max_match_count and best_match:
            if len(question) < len(best_match):
                best_match = question
    
    if max_match_count >= 1:
        return best_match, knowledge_base[best_match], max_match_count
    else:
        return None, "抱歉，未找到相关答案，请尝试其他问题", 0

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox


def main_cli():
    print("=" * 60)
    print("        人工智能基础问答系统")
    print("=" * 60)
    print("欢迎使用AI基础问答系统！")
    print("您可以提出关于人工智能、机器学习、深度学习等方面的问题。")
    print("输入'退出'或'quit'即可结束对话。")
    print("=" * 60)
    
    user_history = []
    
    while True:
        user_input = input("\n请输入您的问题：").strip()
        
        if user_input in ['退出', 'quit', 'exit', 'q']:
            print("\n感谢使用人工智能基础问答系统，再见！")
            break
        
        if not user_input:
            print("请输入有效的问题。")
            continue
        
        user_history.append(user_input)
        
        matched_question, answer, match_count = match_question(user_input)
        
        print("\n" + "=" * 60)
        if matched_question:
            print(f"匹配度最高的问题：{matched_question}")
            print(f"匹配关键词数量：{match_count}")
            print("-" * 60)
        print(f"回答：{answer}")
        print("=" * 60)
    
    print("\n您的提问记录：")
    for i, question in enumerate(user_history, 1):
        print(f"{i}. {question}")


class AIQAGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("人工智能基础问答系统")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        self.user_history = []
        
        self.setup_ui()
    
    def setup_ui(self):
        style = ttk.Style()
        style.configure("Title.TLabel", font=("微软雅黑", 16, "bold"))
        style.configure("Question.TLabel", font=("微软雅黑", 10))
        style.configure("Answer.TLabel", font=("微软雅黑", 10))
        style.configure("Submit.TButton", font=("微软雅黑", 10, "bold"))
        
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        title_label = ttk.Label(main_frame, text="人工智能基础问答系统", style="Title.TLabel")
        title_label.pack(pady=(0, 20))
        
        intro_label = ttk.Label(main_frame, text="欢迎使用AI基础问答系统！\n您可以提出关于人工智能、机器学习、深度学习等方面的问题。", font=("微软雅黑", 10))
        intro_label.pack(pady=(0, 15))
        
        question_frame = ttk.Frame(main_frame)
        question_frame.pack(fill=tk.X, pady=(0, 15))
        
        question_label = ttk.Label(question_frame, text="请输入您的问题：", style="Question.TLabel")
        question_label.pack(side=tk.LEFT, padx=(0, 10))
        
        self.question_entry = ttk.Entry(question_frame, width=60, font=("微软雅黑", 11))
        self.question_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.question_entry.bind("<Return>", self.submit_question)
        
        submit_button = ttk.Button(question_frame, text="提问", command=self.submit_question, style="Submit.TButton")
        submit_button.pack(side=tk.RIGHT, padx=(10, 0))
        
        result_frame = ttk.Frame(main_frame)
        result_frame.pack(fill=tk.BOTH, expand=True)
        
        result_notebook = ttk.Notebook(result_frame)
        result_notebook.pack(fill=tk.BOTH, expand=True)
        
        answer_frame = ttk.Frame(result_notebook)
        history_frame = ttk.Frame(result_notebook)
        
        result_notebook.add(answer_frame, text="回答")
        result_notebook.add(history_frame, text="提问记录")
        
        answer_label = ttk.Label(answer_frame, text="回答内容：", style="Answer.TLabel")
        answer_label.pack(anchor=tk.W, pady=(10, 5))
        
        self.answer_text = scrolledtext.ScrolledText(answer_frame, width=80, height=20, font=("微软雅黑", 11))
        self.answer_text.pack(fill=tk.BOTH, expand=True, padx=5)
        self.answer_text.config(state=tk.DISABLED)
        
        history_label = ttk.Label(history_frame, text="您的提问记录：", style="Answer.TLabel")
        history_label.pack(anchor=tk.W, pady=(10, 5))
        
        self.history_text = scrolledtext.ScrolledText(history_frame, width=80, height=20, font=("微软雅黑", 11))
        self.history_text.pack(fill=tk.BOTH, expand=True, padx=5)
        self.history_text.config(state=tk.DISABLED)
        
        footer_frame = ttk.Frame(main_frame)
        footer_frame.pack(fill=tk.X, pady=(15, 0))
        
        clear_button = ttk.Button(footer_frame, text="清空", command=self.clear_all)
        clear_button.pack(side=tk.LEFT)
        
        exit_button = ttk.Button(footer_frame, text="退出", command=self.root.quit)
        exit_button.pack(side=tk.RIGHT)
    
    def submit_question(self, event=None):
        user_input = self.question_entry.get().strip()
        
        if not user_input:
            messagebox.showwarning("提示", "请输入有效的问题！")
            return
        
        self.user_history.append(user_input)
        self.question_entry.delete(0, tk.END)
        
        matched_question, answer, match_count = match_question(user_input)
        
        self.answer_text.config(state=tk.NORMAL)
        self.answer_text.delete(1.0, tk.END)
        
        if matched_question:
            self.answer_text.insert(tk.END, "匹配度最高的问题：" + matched_question + "\n\n")
            self.answer_text.insert(tk.END, "匹配关键词数量：" + str(match_count) + "\n\n")
            self.answer_text.insert(tk.END, "-" * 50 + "\n\n")
        
        self.answer_text.insert(tk.END, "回答：\n" + answer)
        self.answer_text.config(state=tk.DISABLED)
        
        self.update_history()
    
    def update_history(self):
        self.history_text.config(state=tk.NORMAL)
        self.history_text.delete(1.0, tk.END)
        
        if self.user_history:
            for i, question in enumerate(self.user_history, 1):
                self.history_text.insert(tk.END, f"{i}. {question}\n\n")
        else:
            self.history_text.insert(tk.END, "暂无提问记录")
        
        self.history_text.config(state=tk.DISABLED)
    
    def clear_all(self):
        self.question_entry.delete(0, tk.END)
        self.answer_text.config(state=tk.NORMAL)
        self.answer_text.delete(1.0, tk.END)
        self.answer_text.config(state=tk.DISABLED)
        self.history_text.config(state=tk.NORMAL)
        self.history_text.delete(1.0, tk.END)
        self.history_text.insert(tk.END, "暂无提问记录")
        self.history_text.config(state=tk.DISABLED)
        self.user_history = []


def main():
    root = tk.Tk()
    app = AIQAGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()