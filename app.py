from flask import Flask, render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime,date

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tabi.db'
db = SQLAlchemy(app)

#項目定義
class Post(db.Model):
  id = db.Column(db.Integer,primary_key=True)
  title = db.Column(db.String(50),nullable=False)
  genre = db.Column(db.Integer,nullable=False)
  due = db.Column(db.DateTime,nullable=False)
  adress = db.Column(db.String(100))
  detail = db.Column(db.String(300))



@app.route('/',methods=['GET','POST'])
def index():
  if request.method == 'GET':
    posts = Post.query.order_by(Post.due).all()
    return render_template('index.html',posts=posts,today=date.today())

  else:
    title = request.form.get('title')
    genre = request.form.get('genre')
    due = request.form.get('due')
    adress = request.form.get('adress')
    detail = request.form.get('detail')

    due = datetime.strptime(due, '%Y-%m-%dT%H:%M')
    new_post = Post(title=title, genre=genre, due=due, adress=adress, detail=detail)

    db.session.add(new_post)
    db.session.commit()
    return redirect('/')

@app.route('/create')
def create():
  return render_template('create.html')

@app.route('/detail/<int:id>')
def read(id):
  post = Post.query.get(id)

  return render_template('detail.html', post=post)

@app.route('/delete/<int:id>')
def delete(id):
  post = Post.query.get(id)

  db.session.delete(post)
  db.session.commit()
  return redirect('/')

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    post = Post.query.get(id)
    if request.method == 'GET':
        return render_template('update.html', post=post)
    else:
        post.title = request.form.get('title')
        post.genre = request.form.get('genre')
        post.due = datetime.strptime(request.form.get('due'), '%Y-%m-%dT%H:%M')
        post.adress = request.form.get('adress')
        post.detail = request.form.get('detail')

        db.session.commit()
        return redirect('/')

@app.route('/explanation')
def explanation():
  return render_template('explanation.html')

@app.route('/move', methods=['GET'])
def move():
  post_all = Post.query.order_by(Post.due).all()
  return render_template('move.html',post_all=post_all)

@app.route('/food', methods=['GET'])
def food():
  post_all = Post.query.order_by(Post.due).all()
  return render_template('food.html',post_all=post_all)

@app.route('/sightseeing', methods=['GET'])
def sightseeing():
  post_all = Post.query.order_by(Post.due).all()
  return render_template('sightseeing.html',post_all=post_all)

@app.route('/hotel', methods=['GET'])
def hotel():
  post_all = Post.query.order_by(Post.due).all()
  return render_template('hotel.html',post_all=post_all)

@app.route('/el', methods=['GET'])
def el():
  post_all = Post.query.order_by(Post.due).all()
  return render_template('else.html',post_all=post_all)

if __name__ == "__main__":
    app.run(debug=True)