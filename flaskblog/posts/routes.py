import bleach  # secure against script injection by stripping html tags
from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required

from flaskblog import db
from flaskblog.models import Post, Tag
from flaskblog.posts.forms import PostForm

posts = Blueprint('posts', __name__)


@posts.route("/post/new", methods = ['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        cleaned_content = bleach.clean(form.content.data, tags = bleach.sanitizer.ALLOWED_TAGS + ['p', 's'])

        post = Post(title = form.title.data, content = cleaned_content, author = current_user)
        tags = Tag(name = form.tag.data)
        post.tag.append(tags)

        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title = 'New Post',
                           form = form, legend = 'New Post')


# for viewing a selected post
@posts.route("/post/<int:post_id>")  # passing variable post_id to the url - post_id is an Integer
def post(post_id):
    post = Post.query.get_or_404(
        post_id)  # get_or_404 method gets the post with the post_id and if it doesn't exist it returns a 404 error (page doesn't exist)

    return render_template('post.html', title = post.title, post = post)


@posts.route("/post/<int:post_id>/update", methods = ['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)

    if post.author != current_user:
        abort(403)  # abort function is for showing the passed error page (error 403 - forbidden page)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = bleach.clean(form.content.data, tags=bleach.sanitizer.ALLOWED_TAGS + ['p', 's'])

        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post', post_id = post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content

    return render_template('create_post.html', title = 'Update Post',
                           form = form, legend = 'Update Post')


@posts.route("/post/<int:post_id>/delete", methods = ['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)  # abort function is for showing the passed error page (error 403 - forbidden page)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))
