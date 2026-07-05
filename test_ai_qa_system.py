import unittest
from ai_qa_system import knowledge_base, extract_keywords, match_question

class TestQA(unittest.TestCase):
    
    def test_knowledge_base_length(self):
        self.assertEqual(len(knowledge_base), 20)
    
    def test_extract_keywords_chinese(self):
        keywords = extract_keywords("什么是人工智能？")
        self.assertIn('人', keywords)
        self.assertIn('工', keywords)
        self.assertIn('智', keywords)
        self.assertIn('能', keywords)
    
    def test_extract_keywords_english(self):
        keywords = extract_keywords("Python在AI中的作用")
        self.assertIn('python', keywords)
        self.assertIn('ai', keywords)
    
    def test_extract_keywords_stopwords(self):
        keywords = extract_keywords("什么是机器学习？")
        self.assertNotIn('什', keywords)
        self.assertNotIn('么', keywords)
        self.assertNotIn('是', keywords)
    
    def test_match_exact(self):
        matched_q, answer, _ = match_question("什么是人工智能？")
        self.assertEqual(matched_q, "什么是人工智能？")
        self.assertIn("人工智能", answer)
    
    def test_match_partial(self):
        matched_q, answer, _ = match_question("机器学习是什么")
        self.assertEqual(matched_q, "什么是机器学习？")
        self.assertIn("机器学习", answer)
    
    def test_match_ai(self):
        matched_q, answer, _ = match_question("AI是什么")
        self.assertEqual(matched_q, "什么是人工智能？")
    
    def test_match_deep_learning(self):
        matched_q, answer, _ = match_question("深度学习和机器学习的区别")
        self.assertIsNotNone(matched_q)
        self.assertIn("学习", answer)
    
    def test_match_supervised(self):
        matched_q, answer, _ = match_question("什么是监督学习")
        self.assertEqual(matched_q, "什么是监督学习？")
    
    def test_match_unsupervised(self):
        matched_q, answer, _ = match_question("非监督学习有哪些方法")
        self.assertEqual(matched_q, "什么是非监督学习？")
    
    def test_no_match(self):
        matched_q, answer, _ = match_question("今天天气怎么样")
        self.assertIsNone(matched_q)
        self.assertIn("未找到答案", answer)

if __name__ == '__main__':
    unittest.main(verbosity=2)