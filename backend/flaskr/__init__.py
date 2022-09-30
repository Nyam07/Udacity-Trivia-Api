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

    cors = CORS(app, resources={"/home/*": {"origins": "*"}})
    # CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type, Authorization, true')
        response.headers.add(
            'Access-Controll-Allow-Methods',
            'GET, PUT, POST, DELETE, OPTIONS')

        return response

    # GET ALL CATEGORIES
    @app.route('/categories')
    def get_categories():

        my_categories = format_categories()

        if len(my_categories) == 0:
            abort(400)

        return jsonify({
            'categories': my_categories
        })

    # GET ALL QUESTIONS
    @app.route('/questions')
    def get_questions():
        try:
            all_questions = Question.query.order_by(Question.id).all()

            current_questions = paginate_questions(request, all_questions)

            if len(current_questions) == 0:
                abort(404)

            my_categories = format_categories()

            if len(my_categories) == 0:
                abort(404)

            return jsonify({
                'questions': current_questions,
                'total_questions': len(all_questions),
                'categories': my_categories,
                'currentCategory': my_categories[1]

            })
        except Exception as e:
            print("Exception", e)
            abort(400)

    # DELETE A QUESTION
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter(
                Question.id == question_id).one_or_none()

            if question is None:
                abort(404)

            question.delete()

            return jsonify({
                'success': True,
                'deleted_question': question_id
            })
        except Exception as e:
            print(e)
            abort(404)

    # ADD NEW QUESTION AND SEARCH FOR A QUESTION
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
                questions = Question.query.order_by(
                    Question.id).filter(
                    Question.question.ilike(
                        "%{}%".format(new_search_term)))

                current_questions = paginate_questions(request, questions)

                quiz = current_questions[0]['category']
                current_category = Category.query.filter(
                    Category.id == quiz).one_or_none()

                return jsonify({
                    'questions': current_questions,
                    'total_questions': len(questions.all()),
                    'current_category': current_category.type
                })

            else:
                question = Question(
                    question=new_question,
                    answer=new_answer,
                    difficulty=new_difficulty,
                    category=new_category)
                question.insert()

                return jsonify({
                    'success': True
                })

        except Exception as e:
            print(e)
            abort(404)

    # GET QUESTIONS BY CATEGORY
    @app.route('/categories/<int:category_id>/questions')
    def get_category_questions(category_id):
        try:
            questions = Question.query.order_by(
                Question.id).filter(
                Question.category == category_id)

            current_questions = paginate_questions(request, questions)
            if len(current_questions) == 0:
                abort(404)
            current_category = Category.query.filter(
                Category.id == category_id).one_or_none()

            return jsonify({
                'questions': current_questions,
                'total_questions': len(questions.all()),
                'current_category': current_category.type
            })
        except Exception as e:
            print(e)
            abort(404)

    # PLAY THE QUIZ GAME
    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        body = request.get_json()
        previous_questions = body.get('previous_questions', None)
        selected_category = body.get('quiz_category', None)
        category_id = selected_category['id']
        try:
            if category_id == 0:
                questions = Question.query.filter(
                    Question.id.notin_(previous_questions)).all()
            else:
                questions = Question.query.filter(
                    Question.id.notin_(previous_questions),
                    Question.category == category_id).all()

            question = random.choice(questions)

            return jsonify({
                'question': question.format(),
            })
        except Exception as e:
            print(e)
            abort(400)




    # ERROR HANDLERS

    @app.errorhandler(404)
    def page_not_found(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'Page not found'
        }), 404

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'Bad Request'
        }), 400

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'Unprocessable'
        }), 422


    return app

