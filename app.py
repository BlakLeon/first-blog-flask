from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import db

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=True)
    content = db.Column(db.Text, nullable=True)
    author = db.Column(db.String(20), nullable=False, default='N/a')
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return 'Blog post '+ str(self.id)

all_posts= [
    {
        'title': 'Post 1',
        'content': 'This is the Content of post 1 : LALALALA',
        'author': 'Lefos'
    },
    {
        'title': 'Post 2',
        'content': 'This is the Content of post 2 : LoLALALA'
    }
]

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/posts', methods=['GET','POST'])
def posts():
    if request.method== 'POST':
        post_author = request.form['author']
        post_title = request.form['title']
        post_content = request.form['content']
        new_post = BlogPost(title=post_title, content=post_content,author=post_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    else:
        all_posts= BlogPost.query.order_by(BlogPost.date_posted).all()
        return render_template('posts.html', posts=all_posts)

@app.route('/home/users/<string:name>/posts/<int:id>')
def hello(name,id):
    return f'Hello {name}, your id is: {id}'

@app.route('/posts/delete/<int:id>')
def delete(id):
    post = BlogPost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/posts')

@app.route('/posts/edit/<int:id>', methods=['GET','POST'])
def edit(id):
    post = BlogPost.query.get_or_404(id)
    if request.method=='POST':
        post.title = request.form['title']
        post.content= request.form['content']
        post.author= request.form['author']
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('edit.html', post=post)


if __name__ == '__main__':
    app.run(debug=True)