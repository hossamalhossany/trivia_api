import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


# here i make function to put 10 questions per page
def page(request, questions):
    page_no = request.args.get('page_no', 1, type=int)
    start = (page_no - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    all_questions = [question.format() for question in questions]
    current_question = all_questions[start:end]

    return current_question


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    #
    #   @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    #   # here we used CORS to manage route between backend and frontend
    CORS(app)

    # '''
    # @TODO: Use the after_request decorator to set Access-Control-Allow
    # '''

    @app.after_request
    def after_request(res):
        res.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        res.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return res

        #   '''
        # @TODO:
        # Create an endpoint to handle GET requests
        # for all available categories.
        # '''
        # query all categories
        # make if condition
        # then send to frontend by jsonify

    @app.route('/categories')
    def get_categories():
        # get all categories
        categories_all = Category.query.all()
        categories = {category.id: category.type for category in categories_all}

        if len(categories) > 0:

            return jsonify({
                'success': True,
                'categories': categories
            })
        else:
            abort(404)

        #   '''
        # @TODO:
        # Create an endpoint to handle GET requests for questions,
        # including pagination (every 10 questions).
        # This endpoint should return a list of questions,
        # number of total questions, current category, categories.
        #
        # TEST: At this point, when you start the application
        # you should see questions and categories generated,
        # ten questions per page and pagination at the bottom of the screen for three pages.
        # Clicking on the page numbers should update the questions.
        # '''
        # here we get all questions , current question , total of questions and categories

    @app.route('/questions')
    def get_questions():

        # get all questions
        questions_all = Question.query.all()

        # get current question
        current_question = page(request, questions_all)

        # get all categories
        categories_all = Category.query.all()
        categories = {category.id: category.type for category in categories_all}

        return jsonify({
            'success': True,
            'questions': current_question,
            'total_questions': len(questions_all),
            'categories': categories,

        })

        #   '''
        # @TODO:
        # Create an endpoint to DELETE question using a question ID.
        #
        # TEST: When you click the trash icon next to a question, the question will be removed.
        # This removal will persist in the database and when you refresh the page.
        # '''
        # here i delete question by delete method using question_id

    @app.route('/questions/<question_id>', methods=['DELETE'])
    def delete(question_id):
        question = Question.query.get(question_id)
        question.delete()
        return jsonify({'success': True, 'deleted': question_id})

    #
    #   '''
    # @TODO:
    # Create an endpoint to POST a new question,
    # which will require the question and answer text,
    # category, and difficulty score.
    #
    # TEST: When you submit a question on the "Add" tab,
    # the form will clear and the question will appear at the end of the last page
    # of the questions list in the "List" tab.
    # '''
    # here we add new question

    @app.route("/questions", methods=['POST'])
    def add_new_question():
        body = request.get_json()

        question = body.get('question')
        answer = body.get('answer')
        difficulty = body.get('difficulty')
        category = body.get('category')

        question = Question(question=question, answer=answer,
                            difficulty=difficulty, category=category)
        try:
            question.insert()

            return jsonify({'success': True, 'created': question.id})
        except:
            abort(422)

        #     '''
        # @TODO:
        # Create a POST endpoint to get questions based on a search term.
        # It should return any questions for whom the search term
        # is a substring of the question.
        #
        # TEST: Search by any phrase. The questions list will update to include
        # only question that include that string within their question.
        # Try using the word "title" to start.
        # '''
        #   here we search question

    @app.route('/questions/search', methods=['POST'])
    def search_question():
        body = request.get_json()
        searchTerm = body.get('searchTerm', None)

        # get all questions
        questions_all = Question.query.filter(Question.question.ilike(f'%{searchTerm}%')).all()
        # get all questions by page
        current_question = page(request, questions_all)

        # get all categories
        categories_all = Category.query.all()
        categories = {category.id: category.type for category in categories_all}

        return jsonify({
            'success': True,
            'questions': current_question,
            'current_category': categories,
            'total_questions': len(questions_all)
        })

        #     '''
        # @TODO:
        # Create a GET endpoint to get questions based on category.
        #
        # TEST: In the "List" tab / main screen, clicking on one of the
        # categories in the left column will cause only questions of that
        # category to be shown.
        # '''
        # here we get question by category_id

    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_based_on_category(category_id):

        questions_all = Question.query.filter(Question.category == str(category_id)).all()
        current_question = page(request, questions_all)

        return jsonify({
            'success': True,
            'questions': current_question,
            'total_questions': len(questions_all),
            'current_category': category_id
        })

        #     '''
        # @TODO:
        # Create a POST endpoint to get questions to play the quiz.
        # This endpoint should take category and previous question parameters
        # and return a random questions within the given category,
        # if provided, and that is not one of the previous questions.
        #
        # TEST: In the "Play" tab, after a user selects "All" or a category,
        # one question at a time is displayed, the user is allowed to answer
        # and shown whether they were correct or not.
        # '''

    @app.route('/quizzes', methods=['POST'])
    def quiz():
        body = request.get_json()
        category = body.get('quiz_category')
        previous_questions = body.get('previous_questions')

        if category['type'] == 'click':
            available_question = Question.query.filter(Question.id.notin_(previous_questions)).all()
        else:
            available_question = Question.query.filter_by(category=category['id']).\
                filter(Question.id.notin_(previous_questions)).all()

        new_question = available_question[random.randrange(0, len(available_question))].format() \
            if len(available_question) > 0 else None

        return jsonify({
            'success': True,
            'question': new_question
        })

        #     '''
        # @TODO:
        # Create error handlers for all expected errors
        # including 404 and 422.
        # '''

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "page not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Problem happened"
        }), 422

    return app
