# MiniTwitter

## Overview

MiniTwitter is a simple social media application built using Flask, a Python web framework. It allows users to sign up, log in, and interact with other users by posting messages on their profile and viewing a feed of all posts. The application also includes features such as user profiles, profile images, and a discovery page to explore other users.

## Demo

[Demo Video]()

## Development Environment

- Python 3.11
- Flask 2.3.2
- SQLite database

## Features

- User authentication: Users can sign up and log in to the application.
- User profiles: Each user has a profile page displaying their username, description, and profile image.
- Profile images: Users can upload and display profile images.
- Post creation: Users can create posts and share them with other users.
- Feed: Users can view a feed of all posts in chronological order.
- Discovery: Users can explore other users and their profiles.

## Getting Started

1. Clone the repository:

```shell
   git clone https://github.com/your-username/MiniTwitter.git
```

Install the required dependencies:

```shell
pip install -r requirements.txt
```

Initialize the SQLite database:


```shell
python app.py init-db
```

Run the application:

```shell
python app.py
```

Open your web browser and navigate to http://localhost:5000 to access MiniTwitter.

Configuration

- DATABASE: The path to the SQLite database file (twitter.db by default).
- SECRET_KEY: The secret key used for session encryption and security. Change this to a secure, random value in production.

Future Enhancements

- Improved UI/UX: Enhance the styling and layout of the application for a better user experience.
- Real-time updates: Implement real-time updates using websockets to provide instant notifications for new posts or profile changes.
- User interactions: Enable features such as following other users, liking posts, and commenting on posts.
- Hashtags and search functionality: Implement hashtags to categorize posts and enable users to search for specific topics or users.