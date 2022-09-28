# API Development and Documentation Final Project

## Trivia App

Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a webpage to manage the trivia app and play the game, but their API experience is limited and still needs to be built out.

That's where you come in! Help them finish the trivia app so they can start holding trivia and seeing who's the most knowledgeable of the bunch. The application must:

1. Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.
2. Delete questions.
3. Add questions and require that they include question and answer text.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.

# Getting Started
Developers using this project should already have the following installed:
- Python3
- pip
- node

### Backend
Navigate to the backend folder and initialize and activate a virtual environment
For linux systems
`python -m virtualenv env`
`. env/bin/activate`

For windows systems
`python -m virtualenv env`
`. env/scripts/activate`

Run `pip install requirements.txt` to install all required packages needed to run the application

After installing packages run the application with the following commands
`export FLASK_APP=flaskr`
`export FLASK_ENV=development`
`flask run`
The applicaton will startup and run on `http:127.0.0.1:5000/` by default which is a proxy on the frontend.

### Frontend
The project uses NPM to manage software dependencies which relies on package.json located in the frontend directory. Navigate to the frontend and run:
`$ npm install`
This will install necessary node dependencies.
The frontend app wa built using create-react-app. To run the app in development mode use:
` $ npm start`
This will open on http://localhost:3000 in the browser. Edits made will cause the page to reload.

### Tests
To run app test, navigate to the backend folder and run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

## API Reference
### Error handling
When the app enconteres an error, it will return a JSON object in the following format
```{
    "success":False,
    "error":404,
    "message":"Not found"
}```
The api returns 3 types of errors:
``` 400 : Bad Request
    404 : Not Found
    422 : Unprocessable
```

## Endpoints
### GET /categories
- Returns a list of categories
- Does not take any arguments
- Sample: `curl http://127.0.0.1:5000/categories'
- Results:
``` json
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  }
}
```

### GET /questions?page=${integer}
- Gets a list of questions.
- Arguments: `page`-integer
- Returns an object with 10 paginated questions, total questions, all categories and the current category
- Sample: `curl http://127.0.0.1:5000/questions?page=1'
- Results:
``` json
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "currentCategory": "Science",
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
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
    }
  ],
  "total_questions": 19
}
```

### GET /category/${id}/questions
- Returns questions that belong to a specific category.
- Arguments : `id`-integer 
- Returns an object with questions in the specified category, total questions and current category type string
- Sample: `curl http://127.0.0.1:5000/categories/2/questions`
- Results: 
``` json
{
  "current_category": "Art",
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
    }
  ],
  "total_questions": 4
}
```
### DELETE /questions/${id}'
- Deletes the question with the specified id.
- Arguments: `id`-integer
- Returns a success value and the id of the question deleted
- Sample: `curl http://127.0.0.1:5000/questions/23 -X DELETE`
- Results:
``` json
{
  "deleted_question": 23,
  "success": true
}
```
### POST /questions
- Adds a new question
- You need to provide the question, answer, category, difficulty rating.
- Returns a success value.
- Sample: `curl -X POST -H "Content-Type: application/json" -d '{"question":"what is your name", "answer":"Brian Ngatia", "difficulty":"1", "category":"3"}' http://127.0.0.1:5000/questions`
- Results:
``` json
{
  "success": true
}
```

### POST /questions/searchTerm
- Searches for a question with text matching the search Term provided. 
- Returns the questions matching the search term, category, and total number of questions
- Sample: `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"searchTerm":"what"}'`
- Results: 
```json
{
  "current_category": "Entertainment",
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
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
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "Mona Lisa",
      "category": 2,
      "difficulty": 3,
      "id": 17,
      "question": "La Giaconda is better known as what?"
    },
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    },
    {
      "answer": "Blood",
      "category": 1,
      "difficulty": 4,
      "id": 22,
      "question": "Hematology is a branch of medicine involving the study of what?"
    },
    {
      "answer": "Brian Ngatia",
      "category": 3,
      "difficulty": 1,
      "id": 26,
      "question": "what is your name"
    }
  ],
  "total_questions": 9
}
```
### POST /quizzes
- This endpoint allows you to play the game by allowing you to select a random question from a selected category.
- Arguments: previous_questions - list, quiz_category
- Returns a random question object

- Sample: ` curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"quiz_category":{"type":"Geography","id":"3"}, "previous_questions":[13]}'`

- Results: 
```json
{
  "question": {
    "answer": "The Palace of Versailles",
    "category": 3,
    "difficulty": 3,
    "id": 14,
    "question": "In which royal palace would you find the Hall of Mirrors?"
  }
}
```
