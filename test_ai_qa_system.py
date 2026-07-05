import unittest
from ai_qa_system import knowledge_base, extract_keywords, match_question, keywords_set, keywords_to_questions


class TestKnowledgeBase(unittest.TestCase):
    def test_knowledge_base_size(self):
        self.assertGreaterEqual(len(knowledge_base), 15)
        self.assertLessEqual(len(knowledge_base), 20)

    def test_knowledge_base_structure(self):
        for question, answer in knowledge_base.items():
            self.assertIsInstance(question, str)
            self.assertIsInstance(answer, str)
            self.assertTrue(len(question) > 0)
            self.assertTrue(len(answer) > 0)

    def test_knowledge_base_questions(self):
        expected_questions = [
            "什么是人工智能？",
            "什么是机器学习？",
            "什么是深度学习？",
            "机器学习和深度学习的区别是什么？",
            "Python在人工智能中的作用是什么？",
            "什么是神经网络？",
            "什么是监督学习？",
            "什么是非监督学习？",
            "什么是强化学习？",
            "什么是自然语言处理？",
            "什么是图像识别？",
            "什么是数据挖掘？",
            "什么是特征工程？",
            "什么是过拟合？",
            "什么是欠拟合？",
            "什么是梯度下降？",
            "什么是卷积神经网络？",
            "什么是循环神经网络？",
            "什么是Transformer？",
            "人工智能有哪些应用领域？"
        ]
        for expected in expected_questions:
            self.assertIn(expected, knowledge_base)


class TestKeywordExtraction(unittest.TestCase):
    def test_extract_keywords_chinese(self):
        text = "什么是人工智能？"
        keywords = extract_keywords(text)
        self.assertIn("智", keywords)
        self.assertIn("能", keywords)
        self.assertIn("工", keywords)
        self.assertNotIn("什", keywords)
        self.assertNotIn("么", keywords)
        self.assertNotIn("是", keywords)

    def test_extract_keywords_english(self):
        text = "Python在AI中的作用是什么？"
        keywords = extract_keywords(text)
        self.assertIn("python", keywords)
        self.assertIn("ai", keywords)

    def test_extract_keywords_mixed(self):
        text = "什么是Transformer？"
        keywords = extract_keywords(text)
        self.assertIn("transformer", keywords)

    def test_extract_keywords_stop_words(self):
        text = "什么是机器学习和深度学习的区别？"
        keywords = extract_keywords(text)
        self.assertNotIn("什", keywords)
        self.assertNotIn("么", keywords)
        self.assertNotIn("是", keywords)
        self.assertNotIn("和", keywords)
        self.assertNotIn("区", keywords)
        self.assertNotIn("别", keywords)

    def test_extract_keywords_empty(self):
        text = ""
        keywords = extract_keywords(text)
        self.assertEqual(len(keywords), 0)

    def test_extract_keywords_stop_words_only(self):
        text = "什么是什么？"
        keywords = extract_keywords(text)
        self.assertEqual(len(keywords), 0)


class TestKeywordsSet(unittest.TestCase):
    def test_keywords_set_size(self):
        self.assertGreater(len(keywords_set), 0)

    def test_keywords_set_contains_core(self):
        core_keywords = ["智", "能", "工", "学", "习", "深", "度", "神", "经", "网", "络"]
        for keyword in core_keywords:
            self.assertIn(keyword, keywords_set)


class TestKeywordsToQuestions(unittest.TestCase):
    def test_keywords_to_questions_structure(self):
        self.assertGreater(len(keywords_to_questions), 0)
        for keyword, questions in keywords_to_questions.items():
            self.assertIsInstance(keyword, str)
            self.assertIsInstance(questions, list)
            self.assertGreater(len(questions), 0)

    def test_keywords_to_questions_coverage(self):
        all_questions = set()
        for questions in keywords_to_questions.values():
            all_questions.update(questions)
        self.assertEqual(all_questions, set(knowledge_base.keys()))


class TestQuestionMatching(unittest.TestCase):
    def test_exact_match(self):
        question = "什么是人工智能？"
        matched_q, answer, match_count = match_question(question)
        self.assertEqual(matched_q, question)
        self.assertEqual(answer, knowledge_base[question])
        self.assertGreater(match_count, 0)

    def test_partial_match(self):
        question = "机器学习是什么"
        matched_q, answer, match_count = match_question(question)
        self.assertEqual(matched_q, "什么是机器学习？")
        self.assertGreater(match_count, 0)

    def test_synonym_match(self):
        question = "深度学习和机器学习有什么不同"
        matched_q, answer, match_count = match_question(question)
        self.assertEqual(matched_q, "机器学习和深度学习的区别是什么？")
        self.assertGreater(match_count, 0)

    def test_english_term_match(self):
        question = "Python在AI中的作用"
        matched_q, answer, match_count = match_question(question)
        self.assertEqual(matched_q, "Python在人工智能中的作用是什么？")
        self.assertGreater(match_count, 0)

    def test_no_match(self):
        question = "天气怎么样"
        matched_q, answer, match_count = match_question(question)
        self.assertIsNone(matched_q)
        self.assertEqual(answer, "抱歉，未找到相关答案，请尝试其他问题")
        self.assertEqual(match_count, 0)

    def test_empty_question(self):
        question = ""
        matched_q, answer, match_count = match_question(question)
        self.assertIsNone(matched_q)
        self.assertEqual(answer, "抱歉，未找到相关答案，请尝试其他问题")
        self.assertEqual(match_count, 0)

    def test_match_multiple_keywords(self):
        question = "卷积神经网络是什么"
        matched_q, answer, match_count = match_question(question)
        self.assertEqual(matched_q, "什么是卷积神经网络？")
        self.assertGreaterEqual(match_count, 3)

    def test_match_with_stop_words(self):
        question = "我想了解监督学习"
        matched_q, answer, match_count = match_question(question)
        self.assertEqual(matched_q, "什么是监督学习？")
        self.assertGreater(match_count, 0)

    def test_negative_prefix_match(self):
        question = "非监督学习有哪些方法"
        matched_q, answer, match_count = match_question(question)
        self.assertEqual(matched_q, "什么是非监督学习？")
        self.assertGreater(match_count, 0)

    def test_transformer_match(self):
        question = "Transformer是什么"
        matched_q, answer, match_count = match_question(question)
        self.assertEqual(matched_q, "什么是Transformer？")
        self.assertGreater(match_count, 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)