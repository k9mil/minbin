from app import db


class Paste(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    uuid = db.Column(db.String, unique=True)
    paste_time = db.Column(db.DateTime)
    expire_time = db.Column(db.DateTime)

    def __repr__(self):
        return f"Paste: {self.content} uuid: {self.uuid}"