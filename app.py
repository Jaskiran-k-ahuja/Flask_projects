from flask import Flask,render_template,url_for,request,redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from datetime import datetime
from flask_migrate import Migrate

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:march21%40postgres@localhost:5432/taskmanager'
# engine=create_engine('postgresql://postgres:march21postgres@localhost:5432/taskmanager')
# app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///test.db'


db=SQLAlchemy(app)
migrate = Migrate(app, db)
class todo(db.Model):
    __tablename__ = 'Task-manager'
    id=db.Column(db.Integer,primary_key=True)
    content=db.Column(db.String(200),nullable=False)
    date_created=db.Column(db.DateTime,default=datetime.utcnow)
    
    
    def __repr__(self):
        return '<Task %r>' % self.id
    
    
    
@app.route('/',methods=['POST','GET'])
def index():    
    if request.method=='POST':
        task_content=request.form['content']
        new_task=todo(content=task_content)
        
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'
        # return 'post working'+task_content
    else:
        tasks=todo.query.order_by(todo.date_created).all()
        return render_template('index.html',tasks=tasks)
    
@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete=todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "There was a problem deleting that task"
    
@app.route('/update/<int:id>',methods=['POST','GET'])
def update(id):
    task_to_update=todo.query.get_or_404(id)
    if request.method=='POST':
        task_to_update.content=request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'These is a problem with update'
    else:
        
        return render_template('update.html',task=task_to_update)
    
    
@app.route('/postman',methods=['POST','GET'])
def postman():
    if request.method=='POST':
        return jsonify(message="This is post request", status=201)
    
    elif request.method == 'GET':
        response = {
            "name": "jaskiran",
            "profession": "software engineer",
            "company": "xyz"
        }
        return jsonify(message="This is post request", status=200)
    
    
    
        
if __name__=='__main__':
    app.run(debug=True)