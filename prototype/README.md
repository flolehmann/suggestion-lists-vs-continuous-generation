# Description

This project is a prototype for interacting with generated text. <br>
At the moment there are two different tasks and 3 different interaction methods implemented to fulfill the tasks.
Some data from the tasks is logged in the backend part and other each tasks there are some questions.

# How to Run

## Config

Set the url to your backend in `/frontend/App.js`

## Run w/o docker
Start two seperate terminals.
In the first one go to the backend (`cd backend`) and run `python app.py`. <br>
In the second one got to the frontend (`cd frontend`) and run `npm start`.

It is now available on `http://localhost:3000/`.

##Not recommended: Run with docker
First run `docker-compose build` to build the project. <br>
Then run `docker-compose up` to run the project.

It is now available on `http://localhost:8080/`.

