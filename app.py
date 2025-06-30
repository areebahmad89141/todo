from flask import Flask,render_template ,request,redirect,url_for,flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime,timezone

app = Flask(__name__)
app.secret_key = 'supersecretkey123'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200), nullable = False)
    desc = db.Column(db.String(500), nullable = False)
    date_created = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    def __repr__(self):
        return f"{self.sno},{self.title}"

@app.route('/', methods =['GET','POST'])
def home():
    if request.method =="POST":
        title = request.form['title']
        desc = request.form['Desc']
        todo = Todo(title = title, desc = desc)
        db.session.add(todo)
        db.session.commit()
        return redirect(url_for('home'))
    allTodo = Todo.query.all()
    return render_template('index.html', allTodo=allTodo)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/search/' , methods =['GET','POST'])
def search():
    if request.method =='POST':
        sno = request.form['sno']
        todo = Todo.query.filter_by(sno=sno).first()

        if todo:
            return render_template('search.html',todo=todo)
        else:
            flash(f"No todo item found with sno {sno}. Please try again.", "error")
            return redirect(url_for('search'))


    return render_template('search.html',todo=None)


@app.route('/update/<int:sno>', methods =['GET','POST'])
def update(sno):
    if request.method =="POST":
        title = request.form['title']
        desc = request.form['Desc']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect('/')

    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo=todo)


@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()

    return redirect('/')



if __name__  == "__main__":
    app.run(debug=False ,port=8000)
