#API Reference

##Introduction
This is the API documentation, which will describe the different methods and
endpoints in more detail. If you want to know more about the project as a whole,
check out the readme in the root folder.

##Getting Started

  -Base URL: This API can only be run locally, so it isn't hosted as a base URL.
    The backend can be run at `http://127.0.0.1:5000/`, which is also used in
    the frontend as a proxy
  -Authentication: This API does not use any keys or authentication

##Error Handling

If an error occurs, it will be returned as a JSON object in this format:
```
        {
            'success': False,
            'error': 400,
            'message': 'bad request'
        }
```
There are three error types:
  -400: Bad Request
  -404: Resource Not Found
  -422: Not Processable

##Endpoints

###GET / and /categories

  -General:
    -Returns a list of all the categories, success status, and number of total categories
  -Sample: `curl http://127.0.0.1:5000/` or
    `curl http://127.0.0.1:5000/categories`
    ```
    {
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "success": true,
  "total_categories": 6
}
```
###GET /questions

-General:
  -Returns a list of all the categories, questions, success status, and number
    of total questions
  -Questions are paginated by 10
  -User can choose the page number using queries like ` curl
    http://127.0.0.1:5000/questions?page=2`
  -Sample:
  ```
  {
"categories": {
"1": "Science",
"2": "Art",
"3": "Geography",
"4": "History",
"5": "Entertainment",
"6": "Sports"
},
"questions": [
{
  "answer": "Escher",
  "category": 2,
  "difficulty": 1,
  "id": 16,
  "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
},
{
  "answer": "Mona Lisa",
  "category": 2,
  "difficulty": 3,
  "id": 17,
  "question": "La Giaconda is better known as what?"
},
{
  "answer": "One",
  "category": 2,
  "difficulty": 4,
  "id": 18,
  "question": "How many paintings did Van Gogh sell in his lifetime?"
},
{
  "answer": "Jackson Pollock",
  "category": 2,
  "difficulty": 2,
  "id": 19,
  "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
},
{
  "answer": "The Liver",
  "category": 1,
  "difficulty": 4,
  "id": 20,
  "question": "What is the heaviest organ in the human body?"
},
{
  "answer": "Alexander Fleming",
  "category": 1,
  "difficulty": 3,
  "id": 21,
  "question": "Who discovered penicillin?"
},
{
  "answer": "Blood",
  "category": 1,
  "difficulty": 4,
  "id": 22,
  "question": "Hematology is a branch of medicine involving the study of what?"
},
{
  "answer": "Scarab",
  "category": 4,
  "difficulty": 4,
  "id": 23,
  "question": "Which dung beetle was worshipped by the ancient Egyptians?"
},
{
  "answer": "1",
  "category": 5,
  "difficulty": 1,
  "id": 25,
  "question": "a"
},
{
  "answer": "2",
  "category": 5,
  "difficulty": 1,
  "id": 26,
  "question": "b"
}
],
"success": true,
"total_questions": 24
}
```

###POST /questions

-General:
  Uses post methods to search the database for a search term. It is case
  insensitive and uses substrings to allow for greater flexibility. It returns
  the success status, results (as paginated questions), and the number
  of results. If no results are found, a message will display telling the
  user that no results were found and that they should try again.

  -Sample:
    `curl http://127.0.0.1:5000/questions -X POST -H
    "Content-Type: application/json" -d '{'searchTerm': 'Caged'}'`

    ```
    questions":[{"answer":"Maya Angelou","category":4,"difficulty":2,"id":5,
    "question":"Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"}],"success":true,"total_questions":1}
    ```

###GET /categories/<int:category_id>/questions

-General:
  Returns the questions for each category, success status, and number of
  questions in that category. The user will pick by adding
  an integer that represents the category to the URL (see sample below).
  Please consult the /categories endpoint to find the numbers for each category.  
-Sample: `curl http://127.0.0.1:5000/categories/2/questions`
```
{
  "questions": [
    {
      "answer": "Escher",
      "category": 2,
      "difficulty": 1,
      "id": 16,
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    },
    {
      "answer": "Mona Lisa",
      "category": 2,
      "difficulty": 3,
      "id": 17,
      "question": "La Giaconda is better known as what?"
    },
    {
      "answer": "One",
      "category": 2,
      "difficulty": 4,
      "id": 18,
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    },
    {
      "answer": "Jackson Pollock",
      "category": 2,
      "difficulty": 2,
      "id": 19,
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    },
    {
      "answer": "Grandma Moses",
      "category": 2,
      "difficulty": 4,
      "id": 30,
      "question": "Which artist who began painting in her 70s said \"Painting's not important. The important thing is keeping busy\"?"
    }
  ],
  "success": true,
  "total_questions": 5
}
```

###POST /quizzes

-General:
  This endpoint supports the frontend play quiz feature by returning a random
  question from the selected category with the post method. The user selects
  the category, the front end supplies a list of already completed questions,
  and the backend will find a random question in that category that has not
  been used. The user can also select the option ALL (id 0) to get 5 questions
  from all categories.

-Sample:    

`curl http://127.0.0.1:5000/quizzes -X POST -H
'Content-Type: application/json' -d '{"previous_questions":[],"quiz_category":{"type":"Entertainment","id":"5"}}'`

```
{"question":{
    "answer":"Edward Scissorhands",
    "category":5,"difficulty":3,
    "id":6,
    "question":"What was the title of the 1990 fantasy directed
    by Tim Burton about a young man with multi-bladed appendages?"}}
```

###DELETE /questions

-General:
  This allows the user to delete a question from the database permanently.
  The question id is passed into the URL (see sample below) with the delete
  method and then the deleted question's id, other questions from that page,
  the success status, and the total number of questions is returned.

-Sample:  
`curl http://127.0.0.1:5000/questions/33 -X DELETE'`

```
deleted":33,
"questions": [
  {
    "answer": "Tom Cruise",
    "category": 5,
    "difficulty": 4,
    "id": 4,
    "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
  },
  {
    "answer": "Maya Angelou",
    "category": 4,
    "difficulty": 2,
    "id": 5,
    "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
  },
  {
    "answer": "Edward Scissorhands",
    "category": 5,
    "difficulty": 3,
    "id": 6,
    "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
  },
  {
    "answer": "Muhammad Ali",
    "category": 4,
    "difficulty": 1,
    "id": 9,
    "question": "What boxer's original name is Cassius Clay?"
  },
  {
    "answer": "Brazil",
    "category": 6,
    "difficulty": 3,
    "id": 10,
    "question": "Which is the only team to play in every soccer World Cup tournament?"
  },
  {
    "answer": "Uruguay",
    "category": 6,
    "difficulty": 4,
    "id": 11,
    "question": "Which country won the first ever soccer World Cup in 1930?"
  },
  {
    "answer": "George Washington Carver",
    "category": 4,
    "difficulty": 2,
    "id": 12,
    "question": "Who invented Peanut Butter?"
  },
  {
    "answer": "Lake Victoria",
    "category": 3,
    "difficulty": 2,
    "id": 13,
    "question": "What is the largest lake in Africa?"
  },
  {
    "answer": "The Palace of Versailles",
    "category": 3,
    "difficulty": 3,
    "id": 14,
    "question": "In which royal palace would you find the Hall of Mirrors?"
  },
  {
    "answer": "Agra",
    "category": 3,
    "difficulty": 2,
    "id": 15,
    "question": "The Taj Mahal is located in which Indian city?"
  }
],
"success":true,
"total_questions":25
}
```

###POST /add

-Creates a new question from user input with options for question text,
answer text, difficult level (integer), and category (integer). Returns the
success status, id of the created question, 10 (paginated) questions, and the
number of total questions in the database.

-Sample:
  `curl http://127.0.0.1:5000/add -X POST -H "Content-Type: application/json"
  -d '{"question":"a","answer":"1","difficulty":1,"category":1}'`

```
"created": 33,
"questions": [
  {
    "answer": "Tom Cruise",
    "category": 5,
    "difficulty": 4,
    "id": 4,
    "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
  },
  {
    "answer": "Maya Angelou",
    "category": 4,
    "difficulty": 2,
    "id": 5,
    "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
  },
  {
    "answer": "Edward Scissorhands",
    "category": 5,
    "difficulty": 3,
    "id": 6,
    "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
  },
  {
    "answer": "Muhammad Ali",
    "category": 4,
    "difficulty": 1,
    "id": 9,
    "question": "What boxer's original name is Cassius Clay?"
  },
  {
    "answer": "Brazil",
    "category": 6,
    "difficulty": 3,
    "id": 10,
    "question": "Which is the only team to play in every soccer World Cup tournament?"
  },
  {
    "answer": "Uruguay",
    "category": 6,
    "difficulty": 4,
    "id": 11,
    "question": "Which country won the first ever soccer World Cup in 1930?"
  },
  {
    "answer": "George Washington Carver",
    "category": 4,
    "difficulty": 2,
    "id": 12,
    "question": "Who invented Peanut Butter?"
  },
  {
    "answer": "Lake Victoria",
    "category": 3,
    "difficulty": 2,
    "id": 13,
    "question": "What is the largest lake in Africa?"
  },
  {
    "answer": "The Palace of Versailles",
    "category": 3,
    "difficulty": 3,
    "id": 14,
    "question": "In which royal palace would you find the Hall of Mirrors?"
  },
  {
    "answer": "Agra",
    "category": 3,
    "difficulty": 2,
    "id": 15,
    "question": "The Taj Mahal is located in which Indian city?"
  }
],
"success": true,
"total_questions": 26
}
```
