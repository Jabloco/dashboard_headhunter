from app import db
from app.models import Area

db.create_all()

a = Area(hh_id=1, name='city')
db.session.add(a)
db.session.commit()
