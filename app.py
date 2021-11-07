from flask import Flask, render_template, request, redirect, flash, url_for
from flask.helpers import url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:@localhost:5432/project_tracker'
app.config['SECRET_KEY'] = '\x9dA$\xbd\x13\xee`\xa8\x9cg\x8c\n\xc3\x04\xa6t^\xfc\x9c\xb3\x13cJ'

db = SQLAlchemy(app)

class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(length=50))

class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(length=255))


class ProjectTask(db.Model):
    __tablename__ = 'project_tasks'

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'))


db.create_all()


@app.route("/")
def show_projects():
    return render_template("index.html", projects=Project.query.all())

@app.route("/project/<project_id>")
def show_tasks(project_id):
    project = Project.query.where(Project.id == project_id).first()
    tasks = Task.query.join(ProjectTask, (Task.id == ProjectTask.task_id) & (ProjectTask.project_id == project_id)).all()

    return render_template("project-tasks.html", project=project, tasks=tasks)

@app.route("/add/project", methods=["POST"])
def add_project():
    project_title = request.form['project-title']

    if not project_title:
        flash("Enter a title for your new project", "red")
    else:
        existing_project = Project.query.filter(Project.title == project_title).first()
        if existing_project is None:
            project = Project(title=project_title)
            db.session.add(project)
            db.session.commit()
            flash("Project added successfully!", "green")
        else:
            flash("This Project already exists!", "red")
        
    return redirect(url_for("show_projects"))

@app.route("/add/task/<project_id>", methods=["POST"])
def add_task(project_id):
    task_desc = request.form['task-description']
    if not task_desc:
        flash("Please enter a description for your task!", "red")
    else:
        existing_task = Task.query.join(ProjectTask, 
        (Task.id == ProjectTask.task_id) & 
        (ProjectTask.project_id == project_id) &
        (Task.description == task_desc)).first()

        if existing_task is None:
            task = Task(description=task_desc)
            db.session.add(task)
            db.session.flush()
            task_id = task.id

            project_task = ProjectTask(project_id=project_id, task_id=task_id)
            db.session.add(project_task)
            db.session.commit()

            flash("Task added successfully!", "green")
        else:
            flash("Task for this project already exists!", "red")

    return redirect(url_for("show_tasks", project_id=project_id))

@app.route("/delete/task/<task_id>")
def delete_task(task_id):

    project_task = ProjectTask.query.filter(ProjectTask.task_id == task_id).first()
    project_id = project_task.project_id
    db.session.delete(project_task)

    task = Task.query.filter(Task.id == task_id).first()
    db.session.delete(task)
    db.session.commit()
    flash("Task deleted successfully!", "green")

    return redirect(url_for("show_tasks", project_id=project_id))

@app.route("/delete/project/<project_id>")
def delete_project(project_id):

    project_tasks = ProjectTask.query.filter(ProjectTask.project_id == project_id).all()

    tasks = Task.query.join(ProjectTask,
        (Task.id == ProjectTask.task_id) &
        (ProjectTask.project_id == project_id)).all()

    for pt in project_tasks:
        db.session.delete(pt)

    for t in tasks:
        db.session.delete(t)

    project = Project.query.filter(Project.id == project_id).first()
    db.session.delete(project)
    db.session.commit()
    flash("Project deleted successfully!", "green")

    return redirect(url_for("show_projects"))

    

    db.session.delete(tasls)
    project = Project.query.filter(Project.id == project_id).first()


app.run(debug=True, host="127.0.0.1", port=3000)