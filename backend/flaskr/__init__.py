import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start: end]
    return current_questions


def get_category_list():
    categories = {}
    category_types = []
    for category in Category.query.all():
        categories[category.id] = category.type
        category_types.append(category.type)
    return categories, category_types


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    cors = CORS(app, resources={r'/*': {'origins': '*'}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, POST, DELETE')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response

    @app.route('/')
    @app.route('/categories')
    def get_categories(jsonResponse=True):
        categories, category_types = get_category_list()

        if len(categories) == 0:
            abort(404)

        if jsonResponse:
            return jsonify({
                'success': True,
                'categories': categories,
                'total_categories': len(categories)
            })
        else:
            return category_types

    @app.route('/questions', methods=['GET'])
    def get_paginated_questions():
        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, selection)
        categories = get_category_list()

        if (len(current_questions) == 0):
            abort(404)

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(Question.query.all()),
            'categories': categories[0]
        })

    @app.route('/questions', methods=['POST'])
    def search_questions():
        body = request.get_json()
        search = body.get('searchTerm')

        try:
            results = Question.query.filter(Question.question.ilike('%{}%'.
                                            format(search)))
            display = paginate_questions(request, results)

            if len(results.all()) > 0:
                return jsonify({
                    'success': True,
                    'questions': display,
                    'total_questions': len(results.all())
                })
            else:
                display = [{'question':
                            'No results found. Please search again'}]
                return jsonify({
                    'success': False,
                    'questions': display,
                    'total_questions': len(results.all())
                })
        except Exception as ex:
            print(ex)
            abort(422)

    @app.route('/categories/<int:category_id>/questions')
    def show_cat_questions(category_id):
        try:
            questions = Question.query.filter(Question.category == category_id)
            question_list = paginate_questions(request, questions)

            if (len(question_list) == 0):
                abort(404)

            return jsonify({
                'success': True,
                'questions': question_list,
                'total_questions': len(questions.all())
            })

        except Exception as ex:
            print(ex)
            abort(422)

    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        body = request.get_json()
        category = body.get('quiz_category', None)
        previous_questions = body.get('previous_questions', None)
        if category['id'] == 0:
            questions = Question.query.filter(
                Question.id.notin_(previous_questions))
        else:
            questions = Question.query.filter(
                Question.id.notin_(previous_questions),
                Question.category == category['id']).all()
        post = []
        ids = [question.id for question in questions]

        if len(ids) > 0:
            randomNo = random.choice(ids)
            pick = Question.query.filter(Question.id == randomNo)
            previous_questions.append(pick)
            format = [question.format() for question in pick]
            post.append(format)

            return jsonify({'question': post[0][0]})
        else:
            return jsonify({"question": {"question": "No questions left"}})

    @app.route('/add', methods=['POST'])
    def create_question():
        body = request.get_json()

        new_question = body.get('question', None)
        new_answer = body.get('answer', None)
        new_difficulty = body.get('difficulty', None)
        new_category = body.get('category', None)

        try:
            entry = Question(question=new_question, answer=new_answer,
                             difficulty=new_difficulty, category=new_category)
            entry.insert()

            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, selection)

            return jsonify({
                'success': True,
                'created': entry.id,
                'questions': current_questions,
                'total_questions': len(selection)
            })

        except Exception as ex:
            print(ex)
            abort(422)

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_book(question_id):
        try:
            question = Question.query.filter(Question.id == question_id).\
                one_or_none()

            if question is None:
                abort(404)

            question.delete()
            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, selection)

            return jsonify({
                'success': True,
                'deleted': question_id,
                'questions': current_questions,
                'total_questions': len(selection)
            })
        except Exception as ex:
            print(ex)
            abort(422)

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'bad request'
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'resource not found'
        }), 404

    @app.errorhandler(405)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'method not allowed'
        }), 405

    @app.errorhandler(422)
    def not_found(error):
        return jsonify({
            'success': False,
            'message': 'unprocessable'
        }), 422

    return app
