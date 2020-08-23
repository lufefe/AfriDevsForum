from flask import render_template, request

from flaskblog.main import main
from flaskblog.models import Post, Tag


@main.route("/")
@main.route("/home")
def home():
    # we will use the paginate function to limit the number of posts appearing in the home page - ...
    page = request.args.get('page', 1, type = int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page = page,
                                                                  per_page = 7)  # order the posts by latest date
    tags = Tag.query.distinct(Tag.name).limit(8)
    return render_template('home.html', posts = posts, tags = tags, home = home)


@main.route("/about")
def about():
    return render_template('about.html', title = 'About')
