from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

#  creates an instance of the Flask class.
# Here __name__ represents the current module
app = Flask(__name__)
# /// relative path //// absolute path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return '<Task %r>' % self.id


# Line that tells which url  should trigger following func and here it is index()
@app.route('/', methods=['POST', 'GET'])
# This function will be executed when the root URL is accessed.
def index():
    if request.method=='POST':
        task_content= request.form['content']
        new_task= Todo(content=task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an error in adding your task'
    else:
        # displaying all tasks in table
        tasks= Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)

# Create all tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
