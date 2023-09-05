from app import db


actor_film = db.Table(
    "actor_film",
    db.metadata,
    db.Column("actor_id", db.ForeignKey("actor.id")),
    db.Column("film_id", db.ForeignKey("film.id"))
)


class Actor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    films = db.relationship("Film", secondary="actor_film", back_populates="actors")


class Film(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30))
    description = db.Column(db.Text)
    actors = db.relationship("Actor", secondary="actor_film", back_populates="films")







# Models go here.