"""Blogly application."""

from flask import Flask, render_template, request, redirect, flash

from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = 'secretkey12346'

toolbar = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


# USER ROUTES
@app.route('/')
def home():
    """Home page"""
    posts =Post.query.all()
    return render_template('posts/posts_page.html', posts=posts)



@app.errorhandler(404)
def page_not_found(e):
    """Show 404 NOT FOUND page."""

    return render_template('404.html'), 404


@app.route("/users")
def user_page():

    users = User.query.all()
    return render_template('users/users.html', users=users )

@app.route('/users/new', methods=["GET"])
def new_page():
    """New user form"""
    return render_template('/users/new_page.html')

@app.route("/users/new", methods=["POST"])
def new_user():
    """form submission for a new user"""
    new_user = User(first_name=request.form['first_name'], last_name=request.form['last_name'], image_url=request.form['image_url'] or None)

    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")

@app.route('/users/<int:user_id>')
def show_user(user_id):
    """Show user page"""
    user = User.query.get_or_404(user_id)
    return render_template('/users/show_page.html', user=user)

@app.route('/users/<int:user_id>/edit')
def edit_user(user_id):
    """form to edit page"""
    user = User.query.get_or_404(user_id)
    return render_template('/users/edit_page.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def update_user(user_id):
    """ Form submission for update"""
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']


    db.session.add(user)
    db.session.commit()
    flash(f"{user.full_name} user has been edited.")

    return redirect("/users")

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash(f"{user.full_name} user has been deleted.")

    return redirect("/users")


# POST ROUTES
@app.route('/users/<int:user_id>/posts/new')
def new_post(user_id):
    """Form for new post"""
    user = User.query.get_or_404(user_id)

    tags = Tag.query.all()
    return render_template('posts/new_page.html', user=user, tags=tags)


@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def post_page(user_id):

    user = User.query.get_or_404(user_id)

    tag_ids =[int(n) for n in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    new_post = Post(title = request.form['title'], 
                    content= request.form['content'], user=user, tags =tags)
    db.session.add(new_post)
    db.session.commit()
    
    flash(f"Added Post '{new_post.title}' ")

    return redirect(f'/users/{user_id}')

@app.route('/posts/<int:post_id>')
def show_post_page(post_id):
    """Show Post.."""
    post =Post.query.get_or_404(post_id)
    return render_template("/posts/show_page.html", post=post)

@app.route('/posts/<int:post_id>/edit')
def edit_post_page(post_id):
    """Edit post page.."""
    post =Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    return render_template("/posts/edit_page.html", post=post, tags=tags)

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def show_edit_post_page(post_id):
    """Show edited page"""
    post =Post.query.get_or_404(post_id)

    post.title = request.form['title']
    post.content = request.form['content']
    
    tag_id = [int(n) for n in request.form.getlist("tags")]
    post.tags = Tag.query.filter(Tag.id.in_(tag_id)).all()

    db.session.add(post)
    db.session.commit()

    flash(f"{post.title} post edited")
    return redirect(f"/users/{post.user_id}")

@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def show_delete_page(post_id):
    """To delete page"""
    post =Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()

    flash(f"Post { post.title } has deleted.")
    return redirect(f"/users/{post.user_id}")

# Tags routes....

@app.route('/tags')
def tags_home_page():
    """Show All the tags info"""

    tags = Tag.query.all()
    return render_template("tags/tags_home.html", tags=tags)

@app.route('/tags/new')
def tags_new():
    """Show new tags page form."""

    tags = Tag.query.all()
    posts= Post.query.all()

    return render_template("tags/tags_new.html", posts=posts, tags=tags)

@app.route('/tags/new', methods=["POST"])
def tags_new_page():
    """Show new tag page when handle form submission."""
    post_ids =[int(n) for n in request.form.getlist("posts")]
    posts = Post.query.filter(Post.id.in_(post_ids)).all()
    new_tag = Tag(name=request.form["name"], posts=posts)

    db.session.add(new_tag)
    db.session.commit()

    flash(f"'{new_tag.name}' Tag  added. ")

    return redirect("/tags")

@app.route('/tags/<int:tag_id>')
def tags_show_page(tag_id):
    """Show page with tag."""

    tags= Tag.query.get_or_404(tag_id)
    return render_template('tags/tags_show.html', tags=tags)

@app.route('/tags/<int:tag_id>/edit')
def tags_edit_page(tag_id):
    """Edit tag page """
    tags = Tag.query.get_or_404(tag_id)
    posts= Post.query.all()
    return render_template('tags/tags_edit.html', tags=tags, posts=posts)

@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def tags_edit_post(tag_id):
    tags = Tag.query.get_or_404(tag_id) 
    tags.name =request.form["name"]
    post_ids =[int(n) for n in request.form.getlist("posts")]
    tags.posts = Post.query.filter(Post.id.in_(post_ids)).all()

    db.session.add(tags)
    db.session.commit()

    flash(f"'{tags.name}' tag has been edited..")

    return redirect("/tags")

@app.route('/tags/<int:tag_id>/delete', methods=["POST"])
def tags_delete(tag_id):
    """Submit to delete tags.."""

    tags = Tag.query.get_or_404(tag_id)

    db.session.delete(tags)
    db.session.commit()

    flash(f"'{tags.name}' tag is deleted.")

    return redirect("/tags")




