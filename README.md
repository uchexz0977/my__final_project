This is a project on quiz app using flask python framework and Google Firebase

### Overview

This API allows users to register, log in, and participate in a quiz. It uses Firebase for authentication and Flask for the backend logic.

### Base URL

```
http://127.0.0.1:8000
```

### Endpoints

#### 1. **User Registration**

- **Endpoint**: `/signup`
- **Method**: POST
- **Description**: Registers a new user.
- **Request Parameters**:
  - `email` (string, required): The user's email address.
  - `password` (string, required): The user's password.
- **Request Body**:
  ```json
  {
    "email": "user@example.com",
    "password": "password123"
  }
  ```
- **Response**:
  ```json
  {
    "message": "You have successfully registered!"
  }
  ```

#### 2. **User Login**

- **Endpoint**: `/login`
- **Method**: POST
- **Description**: Logs in an existing user.
- **Request Parameters**:
  - `email` (string, required): The user's email address.
  - `password` (string, required): The user's password.
- **Request Body**:
  ```json
  {
    "email": "user@example.com",
    "password": "password123"
  }
  ```
- **Response**:
  ```json
  {
    "message": "You have successfully logged in!",
    "token": "user_token_here"
  }
  ```

#### 3. **User Logout**

- **Endpoint**: `/logout`
- **Method**: GET
- **Description**: Logs out the current user.
- **Response**:
  ```json
  {
    "message": "You have successfully logged out!"
  }
  ```

#### 4. **Request Password Reset**

- **Endpoint**: `/request-password-reset`
- **Method**: GET
- **Description**: Requests a password reset for the user.
- **Response**:
  ```json
  {
    "message": "Password reset request sent!"
  }
  ```

#### 5. **Quiz**

- **Endpoint**: `/quiz`
- **Method**: GET, POST
- **Description**: Retrieves a quiz question or submits an answer.
- **Request Parameters**:
  - `answers` (string, required for POST): The user's answer to the quiz question.
- **Response**:
  ```json
  {
    "question": "What is the capital of France?",
    "answers": ["Paris", "London", "Berlin", "Madrid"],
    "message": "Correct!",
    "correct_count": 1,
    "attempted_count": 1,
    "total_questions": 10
  }
  ```

#### 6. **Next Question**

- **Endpoint**: `/next`
- **Method**: GET
- **Description**: Retrieves the next quiz question.
- **Response**:
  ```json
  {
    "message": "Next question loaded."
  }
  ```

#### 7. **Restart Quiz**

- **Endpoint**: `/restart`
- **Method**: GET
- **Description**: Restarts the quiz.
- **Response**:
  ```json
  {
    "message": "Quiz restarted."
  }
  ```

### Authentication

- **Method**: Firebase Authentication
- **Description**: All endpoints require a valid Firebase token for authentication.
- **Example**:
  ```
  Authorization: Bearer your_token_here
  ```

### Setup Instructions

1. **Clone the repository**:

   ```sh
   git clone https://github.com/your-repo.git
   cd your-repo
   ```

2. **Create a virtual environment**:

   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies**:

   ```sh
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:

   - Create a `.env` file in the root directory and add the following:
     ```
     FLASK_SECRET_KEY=your_secret_key
     GOOGLE_APPLICATION_CREDENTIALS=path_to_your_firebase_credentials.json
     FIREBASE_API_KEY=your_firebase_api_key
     ```

5. **Run the application**:
   ```sh
   flask run --port=8000
   ```

### Usage Guidelines

- **Register a new user**: Send a POST request to `/signup` with the user's email and password.
- **Log in**: Send a POST request to `/login` with the user's email and password to receive a token.
- **Access the quiz**: Use the token to access the `/quiz` endpoint and participate in the quiz.
- **Log out**: Send a GET request to `/logout` to log out the user.

### Project Architecture

- **app.py**: The main application file containing all routes and logic.
- **templates/**: Directory containing HTML templates for rendering views.
  - `base.html`: Base template for the application.
  - `signup.html`: Template for user registration.
  - `login.html`: Template for user login.
  - `quiz.html`: Template for the quiz.
  - `error.html`: Template for handling server errors.
- **static/**: Directory for static files like CSS and JavaScript.
- **.env**: Environment variables file.
- **requirements.txt**: List of dependencies.

### Examples

#### Register a New User

**Request**:

```sh
curl -X POST http://127.0.0.1:8000/signup -H "Content-Type: application/json" -d '{"email": "user@example.com", "password": "password123"}'
```

**Response**:

```json
{
  "message": "You have successfully registered!"
}
```

#### Log In

**Request**:

```sh
curl -X POST http://127.0.0.1:8000/login -H "Content-Type: application/json" -d '{"email": "user@example.com", "password": "password123"}'
```

**Response**:

```json
{
  "message": "You have successfully logged in!",
  "token": "user_token_here"
}
```

#### Access Quiz

**Request**:

```sh
curl -X GET http://127.0.0.1:8000/quiz -H "Authorization: Bearer your_token_here"
```

**Response**:

```json
{
  "question": "What is the capital of France?",
  "answers": ["Paris", "London", "Berlin", "Madrid"],
  "message": null,
  "correct_count": 0,
  "attempted_count": 0,
  "total_questions": 10
}
```
