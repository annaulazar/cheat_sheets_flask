from app import db

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    is_published = db.Column(db.Boolean, default=True)
    logo = db.Column(db.String(200), default="default_picture.png")

    sheets = db.relationship('Sheet', backref='category', lazy='dynamic')

    def __repr__(self):
        return f'{self.name}'


class Sheet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    text = db.Column(db.Text)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id', ondelete='CASCADE'))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    is_published = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'{self.title}'
