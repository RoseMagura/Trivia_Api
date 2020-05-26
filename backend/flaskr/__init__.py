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

        except:
            abort(422)

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_book(question_id):
        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()

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
        except:
            abort(422)

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'resource not found'
        }), 404

    @app.errorhandler(422)
    def not_found(error):
        return jsonify({
            'success': False,
            'message': 'unprocessable'
        }), 422



    return app



  #
  # '''
  # @TODO:
  # Create a POST endpoint to get questions based on a search term.
  # It should return any questions for whom the search term
  # is a substring of the question.
  #
  # TEST: Search by any phrase. The questions list will update to include
  # only question that include that string within their question.
  # Try using the word "title" to start.
  # '''
  #
  # '''
  # @TODO:
  # Create a GET endpoint to get questions based on category.
  #
  # TEST: In the "List" tab / main screen, clicking on one of the
  # categories in the left column will cause only questions of that
  # category to be shown.
  # '''
  #
  #
  # '''
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
  #
  # '''
  # @TODO:
  # Create error handlers for all expected errors
  # including 404 and 422.
  # '''
