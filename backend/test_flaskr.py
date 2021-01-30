import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    # here i make test for http://127.0.0.1:5000/categories
    def test_get_all_categories(self):
        response = self.client().get("/categories")
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['success'], True)
        self.assertTrue(len(response_data['categories']))

    # here i make test add new question
    def test_add_new_question(self):
        new_question = {
            'question': 'whats your name?? ',
            'answer': 'hossam',
            'difficulty': 2,
            'category': 2
        }
        all_questions = Question.query.all()
        questions_count = len(all_questions)
        response = self.client().post('/questions', json=new_question)
        response_data = json.loads(response.data)
        all_questions = Question.query.all()
        questions_count_after_add = len(all_questions)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['success'], True)
        self.assertEqual(questions_count_after_add, questions_count + 1)

    # here i make test for search ang string at question
    def test_search_questions(self):
        search_term = {'searchTerm': 'n'}
        response = self.client().post('/questions/search', json=search_term)
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['success'], True)
        self.assertIsNotNone(response_data['questions'])
        self.assertIsNotNone(response_data['total_questions'])

    # here i make test for quizzes
    def test_quiz(self):
        new_quiz = {
            'previous_questions': [],
            'quiz_category': {
                'type': 'sport',
                'id': 3
            }
        }
        response = self.client().post('/quizzes', json=new_quiz)
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['success'], True)

    # here i make test questions per category
    def test_questions_on_category(self):
        response = self.client().get('/categories/2/questions')
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['success'], True)
        self.assertTrue(len(response_data['questions']))
        self.assertTrue(response_data['total_questions'])
        self.assertTrue(response_data['current_category'])

    # here i make test for delete question
    def test_delete_question(self):
        question = Question(question='whats your name',
                            answer='hossam',
                            difficulty=2,
                            category=2)
        question.insert()
        question_id = question.id

        response = self.client().delete(f'/questions/{question_id}')
        response_data = json.loads(response.data)

        question = Question.query.filter(Question.id == question.id).one_or_none()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['success'], True)
        self.assertEqual(response_data['deleted'], str(question_id))
        self.assertEqual(question, None)

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        # self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        self.database_path = "postgres://postgres:123@{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
