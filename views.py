from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, current_user
from tables import Comment, Post, User
from __init__ import db

views = Blueprint("views", __name__)

#Calls home html for home page
@views.route("/")
def home():
    return render_template("home.html")

#Calls archive html for archive page
@views.route("/archive")
#Forces user to login to view the page
@login_required
def archive():
    posts = Post.query.order_by(Post.date_created.desc()).all()
    return render_template("archive.html", user = current_user, posts = posts)

#Allows user to create a post
@views.route("/create-post", methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == "POST":
        text = request.form.get('text')

        if not text:
            flash('Post is Empty', category='error')
        else:
            post = Post(text=text, author=current_user.id)
            db.session.add(post)
            db.session.commit()
            flash('Post created!', category='success')
            return redirect(url_for('views.archive'))

    return render_template('create_post.html', user=current_user)


@views.route("/delete-post/<id>")
@login_required
def delete_post(id):
    post = Post.query.filter_by(id=id).first()

    if not post:
        flash("Post does not exist.", category='error')
    elif current_user.id != post.author:
        flash('You do not have permission to delete this post.', category='error')
    else:
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted.', category='success')

    return redirect(url_for('views.archive'))

@views.route('/edit-post/<id>', methods=['GET', 'POST'])
@login_required
def edit_post(id):
    post = Post.query.get_or_404(id)

    if not post:
        flash("Post does not exist.", category='error')
    elif current_user.id != post.author:
        flash('You do not have permission to edit this post.', category='error')

    if request.method == 'POST':
        post.text = request.form['text']
        db.session.commit()
        flash('Post has been edited!', category='success')
        return redirect(url_for('views.archive', id=post.id))

    return render_template('edit_post.html', post=post)


@views.route('/search')
def search():
    query = request.args.get('query')
    posts = Post.query.filter(Post.text.like(f'%{query}%')).all()

    return render_template('search.html', results=posts, query=query)

@views.route('/advanced-search')
def advanced_search():
    return render_template('advanced_search.html')

@views.route('/advanced-results')
def advanced_results():
    query = request.args.get('query')
    name = request.args.get('name')
    if query and not name:
        posts = Post.query.filter(Post.text.like(f'%{query}%')).all()
    if name and not query:
        posts = Post.query.filter(Post.author.like(f'%{name}%')).all()
    if query and name:
        posts = Post.query.filter(Post.text.like(f'%{query}%') & Post.author.like(f'%{name}%')).all()
    return render_template('advanced_results.html', results=posts)

@views.route("/user/<username>")
@login_required
def posts(username):
    user = User.query.filter_by(username = username).first()

    if not user:
        flash("No user with that username")
        return redirect(url_for("views.archive"))
    
    post = Post.query.filter_by(author=user.id).order_by(Post.date_created.desc()).all()
    return render_template("post.html", user=current_user, posts=post, username = username)

@views.route("/create-comment/<post_id>", methods=['POST'])
@login_required
def create_comment(post_id):
    text = request.form.get('text')

    if not text:
        flash("Comment cannot be empty!")
    else:
        post = Post.query.filter_by(id=post_id)
    if post:
        comment = Comment(text = text, author = current_user.id, post_id = post_id)
        db.session.add(comment)
        db.session.commit()
        flash("Successfully commented!", category="success")
    else:
        flash("The post you are attempting to comment on does not exist")
    return redirect(url_for("views.archive"))

@views.route("/delete-comment/<id>")
@login_required
def delete_comment(id):
    comment = Comment.query.filter_by(id=id).first()

    if not comment:
        flash("Comment does not exist.", category='error')
    elif current_user.id != comment.author and current_user.id != comment.post.author:
        flash('You do not have permission to delete this comment.', category='error')
    else:
        db.session.delete(comment)
        db.session.commit()
        flash('Comment deleted.', category='success')

    return redirect(url_for('views.archive'))

@views.route('/edit-comment/<id>', methods=['GET', 'POST'])
@login_required
def edit_comment(id):
    comment = Comment.query.get_or_404(id)

    if not comment:
        flash("Comment does not exist.", category='error')
    elif current_user.id != comment.author:
        flash('You do not have permission to edit this comment.', category='error')

    if request.method == 'POST':
        comment.text = request.form['text']
        db.session.commit()
        flash('Comment has been edited!', category='success')
        return redirect(url_for('views.archive', id=comment.id))

    return render_template('edit_comment.html', comment=comment)
