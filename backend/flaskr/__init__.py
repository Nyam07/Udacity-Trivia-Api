import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

# Method for pagination
def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions

# Method for formating categories
def format_categories():
    all_categories = Category.query.order_by(Category.id).all()

    my_ids = [category.id for category in all_categories]
    my_types = [category.type for category in all_categories]

    # convert to dict
    my_categories = dict(zip(my_ids, my_types))

    return my_categories

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    cors = CORS(app, resources={"/home/*": {"origins":"*"}})
    #CORS(app)


    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, true')
        response.headers.add('Access-Controll-Allow-Methods', 'GET, PUT, POST, DELETE, OPTIONS')

        return response

    @app.route('/categories')
    def get_categories():

        my_categories = format_categories()

        if len(my_categories) == 0:
            abort(400)

        return jsonify({
            'categories':my_categories
        })

    @app.route('/questions')
    def get_questions():
        all_questions = Question.query.order_by(Question.id).all()

        current_questions = paginate_questions(request, all_questions)

        if len(current_questions) == 0:
            abort(404)

        my_categories = format_categories()

        if len(my_categories) == 0:
            abort(400)

        return jsonify({
            'questions': current_questions,
            'total_questions': len(all_questions),
            'categories': my_categories,
            'currentCategory': my_categories[4],

        })

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        question = Question.query.filter(Question.id == question_id).one_or_none()

        if question is None:
            abort(404)

        question.delete()
        
        return jsonify({
            'success': True,
            'deleted_question': question_id
        })

    @app.route('/questions', methods=['POST'])
    def add_question():
        body = request.get_json()
        new_question = body.get("question", None)
        new_answer = body.get("answer", None)
        new_difficulty = body.get("difficulty", None)
        new_category = body.get("category", None)
        new_search_term = body.get("searchTerm", None)

        try:
            if new_search_term:
                questions = Question.query.order_by(Question.id).filter(Question.question.ilike("%{}%".format(new_search_term)))

                current_questions =  paginate_questions(request, questions)

                quiz = current_questions[0]['category']
                current_category = Category.query.filter(Category.id == quiz).one_or_none()

                return jsonify({
                    'questions': current_questions,
                    'total_questions': len(questions.all()),
                    'current_category': current_category.type
                })

            else:
                question = Question(question=new_question, answer=new_answer, difficulty=new_difficulty, category=new_category)
                question.insert()

                return jsonify({
                    'success':True
                })

        except Exception as e:
            print(e)
            abort(422)

    @app.route('/categories/<int:category_id>/questions')
    def get_category_questions(category_id):
        questions = Question.query.order_by(Question.id).filter(Question.category == category_id)

        current_questions = paginate_questions(request, questions)
        if len(current_questions) == 0:
            abort(404)
        current_category = Category.query.filter(Category.id == category_id).one_or_none()

        return jsonify({
            'questions': current_questions,
            'total_questions': len(questions.all()),
            'current_category': current_category.type
        })
        

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    return app

