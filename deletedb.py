from app import models,db

users = models.User.query.all()
for u in users:
    db.session.delete(u)
db.session.commit()