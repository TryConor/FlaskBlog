import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect, abort

# Make a Flask application object called app
app = Flask(__name__)
app.config["DEBUG"] = True
app.config["SECRET_KEY"] = "your secret key"

# Function to open a connection to the database.db file
def get_db_connection():
    # Create connection to the database
    conn = sqlite3.connect('database.db')
    # Allows us to have name-based access to columns
    # The database connection will return rows we can access like regular Python dictionaries
    conn.row_factory = sqlite3.Row
    # Return the connection object
    return conn

# Function to retrieve a post from the database
def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
    conn.close()
    
    if post is None:
        abort(404)
    return post

# Use the app.route() decorator to create a Flask view function called index()
@app.route('/')
def index():
    # Get a connection to the database
    conn = get_db_connection()
    # Execute a query to read all posts from the posts table in db
    posts = conn.execute('SELECT * FROM posts').fetchall()
    # Close connection
    conn.close()
    # Send the posts to the index.html template to be displayed
    return render_template('index.html', posts=posts)

# Route to create a post
@app.route('/create/', methods=('GET', 'POST'))
def create():
    # Determine if the page is being requested with a POST or GET request
    if request.method == 'POST':
        # Get the title and content that was submitted
        title = request.form['title']
        content = request.form['content']
        # Display an error if title or content is not permitted 
        # Else make a database connection and insert the blog post content 
        if not title:
            flash("Title is required")
        elif not content: 
            flash("Content is required")
        else: 
            conn = get_db_connection()
            # Insert data into database 
            conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)', (title, content))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
    return render_template('create.html')

# Create a route to edit a post. Load page with the GET or POST method 
# Pass the post id as a URL parameter
@app.route('/<int:id>/edit/', methods=('GET', 'POST'))
def edit(id):
    # Get the post from the database with a select query for the post with that ID 
    post = get_post(id)
    # Determine if the page was requested with GET or POST 
    # If POST, process the form data. Get the data and validate it. Update the post and redirect to the home page. 
    if request.method == 'POST':
        # Get the title and content 
        title = request.form['title']
        content = request.form['content']
        # If no title or content flash an error message 
        if not title:
            flash("Title is required")
        elif not content:
            flash("Content is required")
        else: 
            conn = get_db_connection()
            conn.execute('UPDATE posts SET title = ?, content = ? WHERE id = ?', (title, content, id))
            conn.commit()
            conn.close()
            # Redirect to the home page
            return redirect(url_for('index'))
    # If GET then display the page
    return render_template('edit.html', post=post)

#create a route to delete a post
#delete will only be processed with a post method 
#the post id is the url parameter
@app.route('/int:id>/delete', methods=('POST',))
def delete(id):
    #get the post
    post = get_post(id)

    #connect to the database
    conn = get_db_connection()

    #execute a delete query 
    conn.execute('Delete from posts WHERE id = ?', (id,))

    #commit and close the connection 
    conn.commit()
    conn.close()

    #flash a success message
    flash('"{}" was succesfully deleted!'.format(post['title']))

    #redirect from the homepage 
    return redirect(url_for('index'))

app.run(port=5008)
