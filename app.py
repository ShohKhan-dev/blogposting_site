from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'

db = SQLAlchemy(app)

class Blogpost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    subtitle = db.Column(db.String(50))
    author = db.Column(db.String(20))
    date_posted = db.Column(db.DateTime)
    content = db.Column(db.Text)

@app.route('/')
def index():
    posts = Blogpost.query.order_by(Blogpost.date_posted.desc()).all()

    return render_template('index.html', posts=posts)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/post/<int:post_id>')
def post(post_id):
    post = Blogpost.query.filter_by(id=post_id).one()

    return render_template('post.html', post=post)


@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    blog_to_update = Blogpost.query.get_or_404(id)
    if request.method == "POST":
        blog_to_update.title = request.form['title']
        blog_to_update.subtitle = request.form['subtitle']
        blog_to_update.author = request.form['author']
        blog_to_update.content = request.form['content']

        try:
            db.session.commit()
            return redirect(url_for('index'))
        except:
            return "There was Problem HEERE!!!"
    else:
        return render_template('update.html', blog_to_update = blog_to_update )


@app.route('/add')
def add():
    return render_template('add.html')

@app.route('/addpost', methods=['POST'])
def addpost():
    title = request.form['title']
    subtitle = request.form['subtitle']
    author = request.form['author']
    content = request.form['content']

    post = Blogpost(title=title, subtitle=subtitle, author=author, content=content, date_posted=datetime.now())

    db.session.add(post)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete(id):
    blog_to_delete = Blogpost.query.get_or_404(id)

    try:
        db.session.delete(blog_to_delete)
        db.session.commit()
        return redirect(url_for('index'))
    except:
        return "There is Problem with deleting Items!!!"


if __name__ == '__main__':
    app.run(debug=True)
