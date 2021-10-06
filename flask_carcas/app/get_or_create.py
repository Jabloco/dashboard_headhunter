from os import name
from app import db
from app.models import Area
import sqlalchemy

def get_or_create(model, **kwargs):
    """
    Делаем запрос в БД, при наличии определенной записи,
    возвращаем ее, при отсутствии, создаем и возвращаем.
    """
    try:
        try:
            a = model.query.filter_by(**kwargs).first()
        except sqlalchemy.exc.InvalidRequestError:
            print("Лишний аргумент!")
            exit()
        if a != None:
            return a, "Exist"
        else:
            a = model(**kwargs)
            db.session.add(a)
            db.session.commit()
            return a, "Created"
    except sqlalchemy.exc.IntegrityError:
        print("Уже существующий аргумент!")
        exit()
        
a, exist = get_or_create(Area, hh_id=1, name="John")
print(a.name, exist)

"""
>>> a, exist = get_or_create(User, username="Mary", email="mary@example.com")
>>> a, exist
Mary Created
"""