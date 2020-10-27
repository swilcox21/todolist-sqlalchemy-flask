from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    done = db.Column(db.Boolean(), unique=False, nullable=False)
    label = db.Column(db.String(120), unique=True, nullable=False)
    user_name = db.Column(db.String(80), unique=False, nullable=False)

    def __repr__(self):
        return '<Todo %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "done": self.done,
            "label": self.label,
            "user_name": self.user_name
        }





class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }