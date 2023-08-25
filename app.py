from flask import Flask, request, redirect, render_template, flash, session, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///blogly_db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'ihaveasecret'


connect_db(app)
db.create_all()


@app.route('/')
def root():
    """Homepage redirects to list of users."""

    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    return render_template('main-homepage.html', posts=posts)
  
# @app.route("/signIn")
# def signed_in():
#     return render_template("signIn.html")
  
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Retrieve the email from the login form
        email = request.form["email"]

        # Store the email in the session
        session["email"] = email

        return redirect("/registration")

    return render_template("login.html")
  
@app.route("/registration", methods=["GET", "POST"])
def registration():
    if request.method == "POST":
        # Retrieve form data
        first_name = request.form["firstName"]
        last_name = request.form["lastName"]
        password = request.form["newPassword"]

        # Render a success page or redirect to a different page
        return render_template("posts/homepage.html")

    # Retrieve the email from the session
    email = session.get("email")

    # Render the registration form
    return render_template("registration.html", email=email)
  
@app.route("/logout")
def logout():
    # Clear the session
    session.clear()

    # Redirect to the login page
    return redirect("/homepage.html")
  
# @app.route(404)
# def page_not_found(e):
#     """404 NOT FOUND page."""

#     return render_template('404.html'), 404
  
#####################################################################
# User routes

@app.route('/users')
def users_index():
    """Show a page with info on all users"""

    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('users/index.html', users=users)


@app.route('/users/new', methods=["GET"])
def users_new_form():
    """Show a form to create a new user"""

    return render_template('users/new.html')


@app.route("/users/new", methods=["POST"])
def users_new():
    """Handle form submission for creating a new user"""

    new_user = User(
        first_name=request.form['first_name'],
        last_name=request.form['last_name'],
        image_url=request.form['image_url'] or None
    )
    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")


@app.route('/users/<int:user_id>')
def users_show(user_id):
    """Show a page with info on a specific user"""

    user = User.query.get_or_404(user_id)
    return render_template('users/show.html', user=user)


@app.route('/users/<int:user_id>/edit')
def users_edit(user_id):
    """Show a form to edit an existing user"""

    user = User.query.get_or_404(user_id)
    return render_template('users/edit.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=["POST"])
def users_update(user_id):
    """Handle form submission for updating an existing user"""

    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect("/users")


@app.route('/users/<int:user_id>/delete', methods=["POST"])
def users_destroy(user_id):
    """Handle form submission for deleting an existing user"""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")
  
#####################################################################
# Post routes

@app.route('/users/<int:user_id>/posts/new')
def posts_new_form(user_id):
    """Show a form to create a new post for a specific user"""

    user = User.query.get_or_404(user_id)
    return render_template('posts/new.html', user=user)
  
  
#####################################################################
# Datbase UI route

@app.route('/db')
def db_debug():
    """Show a page with info on all users"""

    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('db.html', users=users)
  
  
if __name__ == '__main__':
    app.run(debug=True)