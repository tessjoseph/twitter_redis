# 🐦 Twitter Redis Pipeline 🚀

This project is a Twitter-like application built using Redis as the backend data store. It provides basic functionalities such as posting tweets, following other users, and viewing the home timeline.

## 🌟 Features

- **Posting Tweets:** Users can post tweets, which are stored in Redis using a unique tweet ID.
- **Following Users:** Users can follow other users, which is implemented by storing user IDs in a Redis set.
- **Viewing Home Timeline:** Users can view their home timeline, which includes tweets from users they follow. This is implemented by retrieving tweets from followed users' timelines and sorting them by timestamp.

## 🛠️ Technologies Used

- Python 
- Redis 

## ▶️ How to Run

1. Clone the repository.
2. Install the required dependencies (`redis` library for Python).
3. Run the application using `python redis_twitter.py`.
4. Access the application in your web browser at `http://localhost:5000`.

## 🚀 Future Improvements

- Implement user authentication and authorization.
- Add support for direct messaging between users.
- Improve error handling and data validation.

## 🙏 Acknowledgements

This project was inspired by the simplicity and efficiency of Redis as a data store for real-time applications like Twitter.

---
