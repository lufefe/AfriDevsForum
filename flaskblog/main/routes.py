import requests
from flask import Blueprint, redirect
from flask import render_template, request, current_app, g, url_for
from flask_login import current_user
from sqlalchemy import or_

from flaskblog import db
from flaskblog.decorators import admin_required
from flaskblog.models import Post, Tag, User
from flaskblog.posts.forms import SearchForm

main = Blueprint('main', __name__)


@main.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated:
        g.search_form = SearchForm()


# CHECK USER LOCATION - IP ADDRESS.
def get_user_ip(ip_address):
    try:
        response = requests.get(
            "http://ip-api.com/json/{}?fields=status,message,continent,continentCode,country,countryCode,region,regionName,city,zip,lat,lon,timezone,isp,org,as,mobile,proxy,query".format(
                ip_address))
        data = response.json()
        return data
    except Exception as e:
        return "Unknown"


@main.route("/")
@main.route("/home")
def home():
    # TODO: use HTTP_X_FORWARDED_FOR to get ip address on nginx (Production)
    # ip_address = request.remote_addr
    # user_data = get_user_ip(ip_address)

    user_count = db.session.query(User).count()
    post_count = db.session.query(Post).count()
    # we will use the paginate function to limit the number of posts appearing in the home page - ...
    page = request.args.get('page', 1, type = int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page = page,
                                                                  per_page = current_app.config[
                                                                      'FLASKY_POSTS_PER_PAGE'])

    # tags = Tag.query.distinct(Tag.name).limit(8)
    tags = db.session.query(Tag.name).distinct().limit(6)
    return render_template('home.html', posts = posts, tags = tags, user_count = user_count, post_count = post_count)


@main.route("/about")
def about():
    return render_template('about.html', title = 'About')


@main.route("/advertising")
def advertising():
    return render_template('advertising.html', title = 'Advertising')


@main.route("/contact")
def contact():
    return render_template('contactus.html', title = 'Contact Us')


@main.route("/admin")
@admin_required
def admin():
    pass


@main.route('/search_results/<query>')
# @login_required
def search_results(query):
    print(query)
    page = request.args.get('page', 1, type = int)
    query_formatted = "%{}%".format(query)
    query_test = Post.query.filter(or_(Post.title.like(query_formatted), Post.content.like(query_formatted)))

    return render_template('search_results.html', posts = query_test, query = query)


@main.route('/search', methods = ['POST'])
# @login_required
def search():
    query = request.form.get('query')
    if not query:
        return redirect(url_for('main.home'))
    return redirect(url_for('main.search_results', query = query))

#
# @main.route("/")
# def maintenance():
#     return render_template('under_maintenance.html')
