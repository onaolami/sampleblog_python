## Sample Blog App

This is a Sample Blog App that contains routes for a typical blog:

- create post
- get all posts
- get specific post
- search for post
- delete post

- create comment
- get all comments
- delete comment

- create user
- login user

### How to Run the App

- First of all, check the .example.env file, and create a .env for the keys you'll find there.

- Then create a virtual environment and install the necessary dependencies from the requirements.txt

- Now, at the root level of this project, run the following command:

```bash
uvicorn src.main:app --reload
```

In your browser, open the following address to see the docs of this project:

```
localhost:8000/docs
```