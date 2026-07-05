import gradio as gr
from ai_qa_system import knowledge_base, extract_keywords, match_question

def chat_with_qa(question, history):
    user_keywords = extract_keywords(question)
    matched_q, answer, match_count = match_question(question)
    
    response = f"**匹配问题：** {matched_q}\n\n" if matched_q else ""
    response += f"**回答：** {answer}"
    
    return response

def get_welcome_message():
    return """欢迎使用**人工智能基础问答系统**！
    
您可以提出关于人工智能、机器学习、深度学习等方面的问题。

**示例问题：**
- 什么是人工智能？
- 机器学习是什么？
- 深度学习和机器学习的区别？
- Python在AI中的作用？
- 什么是神经网络？

开始提问吧！"""

with gr.Blocks(title="人工智能基础问答系统", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🧠 人工智能基础问答系统")
    
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("## 📚 知识库")
            gr.Markdown(f"包含 **{len(knowledge_base)}** 个人工智能基础问题")
            
            with gr.Accordion("查看所有问题", open=False):
                questions_list = gr.Markdown(
                    "\n".join([f"- {q}" for q in knowledge_base.keys()])
                )
        
        with gr.Column(scale=2):
            chatbot = gr.Chatbot(
                value=[[None, get_welcome_message()]],
                height=500,
                bubble_full_width=False
            )
            
            with gr.Row():
                question_input = gr.Textbox(
                    placeholder="请输入您的问题...",
                    label="问题",
                    scale=4
                )
                submit_btn = gr.Button("提问", scale=1)
            
            with gr.Row():
                clear_btn = gr.Button("清空对话")
    
    def respond(question, chat_history):
        if not question.strip():
            return "", chat_history
        
        user_keywords = extract_keywords(question)
        matched_q, answer, match_count = match_question(question)
        
        response_parts = []
        if matched_q:
            response_parts.append(f"🔍 **匹配问题：** {matched_q}")
            response_parts.append(f"📊 **匹配关键词数：** {match_count}")
            response_parts.append("---")
        response_parts.append(f"💡 **回答：** {answer}")
        
        response = "\n\n".join(response_parts)
        
        chat_history.append((question, response))
        return "", chat_history
    
    submit_btn.click(respond, [question_input, chatbot], [question_input, chatbot])
    question_input.submit(respond, [question_input, chatbot], [question_input, chatbot])
    
    clear_btn.click(
        lambda: [[None, get_welcome_message()]],
        None,
        chatbot
    )

if __name__ == "__main__":
    demo.launch(share=True)