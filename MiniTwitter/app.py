import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session
from PIL import Image, ImageDraw
import random

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# SQLite database initialization
DATABASE = 'twitter.db'


def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            description TEXT,
            profile_image TEXT
        )
        """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        """
    )
    conn.commit()
    conn.close()


# Create a dummy user for the initial sign up
def create_dummy_user():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO users (username, password, description, profile_image)
        VALUES (?, ?, ?, ?)
        """,
        ('dummy', 'password', 'I am a dummy user!', 'dummy.png')
    )
    conn.commit()
    conn.close()


def generate_random_image(user_id):
    # Generate a random RGB color
    color = tuple(random.randint(0, 255) for _ in range(3))

    # Create the 'static/images' directory if it doesn't exist
    os.makedirs('static/images', exist_ok=True)

    # Create a 200x200 image with the random color
    image = Image.new('RGB', (200, 200), color)
    draw = ImageDraw.Draw(image)

    # Save the image with the user_id as the filename
    filename = f"static/images/{user_id}.png"
    image.save(filename)

    return filename


# Check if a user is logged in
def is_logged_in():
    return 'username' in session


# Route for the login page
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, username FROM users
            WHERE username = ? AND password = ?
            """,
            (username, password)
        )
        user = cursor.fetchone()
        conn.close()
        if user:
            session['user_id'] = user[0]
            session['username'] = user[1]
            return redirect(url_for('profile'))
        else:
            error = 'Invalid login credentials'
            return render_template('login.html', error=error)
    return render_template('login.html')


# Route for the signup page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO users (username, password, profile_image)
            VALUES (?, ?, ?)
            """,
            (username, password, f'{username}.png')
        )
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        session['user_id'] = user_id
        session['username'] = username

        # Generate a random image for the user
        image_filename = generate_random_image(user_id)

        return redirect(url_for('profile'))
    return render_template('signup.html')


# Route for the profile page
@app.route('/profile')
def profile():
    if not is_logged_in():
        return redirect(url_for('login'))
    user_id = session['user_id']
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT username, description, profile_image FROM users
        WHERE id = ?
        """,
        (user_id,)
    )
    user = cursor.fetchone()
    cursor.execute(
        """
        SELECT content, created_at FROM posts
        WHERE user_id = ?
        ORDER BY created_at DESC
        """,
        (user_id,)
    )
    posts = cursor.fetchall()
    conn.close()

    # Generate a random image if the user doesn't have one
    if user[2] == f'{user[0]}.png':
        image_filename = generate_random_image(user_id)
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE users
            SET profile_image = ?
            WHERE id = ?
            """,
            (image_filename, user_id)
        )
        conn.commit()
        conn.close()

    return render_template('profile.html', user=user, posts=posts)


# Route for the feed page
@app.route('/feed')
def feed():
    if not is_logged_in():
        return redirect(url_for('login'))
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT username, profile_image, content, created_at FROM posts
        INNER JOIN users ON users.id = posts.user_id
        ORDER BY created_at DESC
        """
    )
    posts = cursor.fetchall()
    conn.close()
    return render_template('feed.html', posts=posts)


# Route for the discover page
@app.route('/discover')
def discover():
    if not is_logged_in():
        return redirect(url_for('login'))
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT username, description, profile_image FROM users
        """
    )
    users = cursor.fetchall()
    conn.close()
    return render_template('discover.html', users=users)


# Logout route
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


if __name__ == '__main__':
    init_db()
    if not os.path.isfile('dummy.png'):
        create_dummy_user()
    app.run(debug=True)
