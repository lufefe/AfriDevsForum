import bleach  # secure against script injection by stripping html tags
from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from sqlalchemy import exc

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
        create_post = Post(title = form.title.data, content = cleaned_content, author = current_user)

        for i in form.tags.data:
            tags = Tag(name = i)  # adds tag to TAG db Table
            create_post.tag.append(tags)  # adds tag to post_tag table with post id.

        db.session.add(create_post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title = 'New Post',
                           form = form, legend = 'New Post')


# for viewing a selected post
@posts.route("/post/<int:post_id>")  # passing variable post_id to the url - post_id is an Integer
def post(post_id):
    # get_or_404 method gets the post with the post_id and if it doesn't exist it returns a 404 error (
    # page doesn't exist)
    view_post = Post.query.get_or_404(post_id)

    return render_template('post.html', title = view_post.title, post = view_post)


@posts.route("/post/<int:post_id>/update", methods = ['GET', 'POST'])
@login_required
def update_post(post_id):
    post_update = Post.query.get_or_404(post_id)

    if post_update.author != current_user:
        abort(403)  # abort function is for showing the passed error page (error 403 - forbidden page)
    form = PostForm()
    if form.validate_on_submit():
        post_update.title = form.title.data
        post_update.content = bleach.clean(form.content.data, tags = bleach.sanitizer.ALLOWED_TAGS + ['p', 's'])
        for i in form.tags.data:
            exists = db.session.query(db.exists().where(Tag.name == i)).scalar()
            if not exists:
                tags = Tag(name = i)  # adds tag to TAG db Table
                post_update.tag.append(tags)  # adds tag to post_tag table with post id.
        try:
            db.session.commit()
            flash('Your post has been updated!', 'success')
        except exc.IntegrityError:
            db.session.rollback()
            flash('Your post has been couldn\'t be updated!', 'warning')

        return redirect(url_for('posts.post', post_id = post_update.id))
    elif request.method == 'GET':
        form.title.data = post_update.title
        form.content.data = post_update.content
        tags = [x.name for i, x in enumerate(post_update.tag.all())]  # loop through all the tags and display them
        form.tags.data = tags

    return render_template('create_post.html', title = 'Update Post',
                           form = form, legend = 'Update Post')


@posts.route("/post/<int:post_id>/delete", methods = ['POST'])
@login_required
def delete_post(post_id):
    post_delete = Post.query.get_or_404(post_id)
    if post_delete.author != current_user:
        abort(403)  # abort function is for showing the passed error page (error 403 - forbidden page)
    db.session.delete(post_delete)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))
