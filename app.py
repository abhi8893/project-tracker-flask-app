from flask import Flask, render_template
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

    return "Project Added Successfully!"

@app.route("/add/task/<project_id>", methods=["POST"])
def add_task(project_id):
    return "Task Added Successfully"


app.run(debug=True, host="127.0.0.1", port=3000)