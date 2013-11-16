from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, Float, \
create_engine, ForeignKey, Enum, Boolean
from sqlalchemy.orm import sessionmaker, relationship, backref, scoped_session

engine = create_engine("sqlite:///garden.db", echo=False)
session = scoped_session(sessionmaker(bind=engine,
                                      autocommit = False,
                                      autoflush = False))

Base = declarative_base()
Base.query = session.query_property()

class Planting(Base):
	__tablename__ = 'plantings'

	id = Column(Integer, primary_key=True)
	name = Column(String(256), nullable=False)
	planted_date = Column(Date)
	completed = Column(Boolean, default=False)

	reminders = relationship('Reminder', backref='planting')
	cultivar_id = Column(Integer, ForeignKey('cultivars.id'))
	cultivar = relationship('Cultivar', backref='plantings')
	harvests = relationship('Harvest', backref='planting')
	group = relationship('Group', backref='plantings')
	group_id = Column(Integer, ForeignKey('groups.id'))


class Reminder(Base)
:	__tablename__ = 'reminders'

	id = Column(Integer, primary_key=True)
	due_date = Column(Date, nullable=False)
	kind = Column(Enum('water', 'fertilize', 'harvest', name='reminder_type',
			nullable=False))
	text = Column(String(256))
	completed_date = Column(Date)
	recurrence = Column(Integer)
	planting_id = Column(Integer, ForeignKey('plantings.id'))



class Cultivar(Base):
	__tablename__ = 'cultivars'

	id = Column(Integer, primary_key=True)
	name = Column(String(256), nullable=False)
	cultivar_type = Column(Enum('tomato', 'broccoli', 'squash', 'lettuce', 
					'other', name="type"), nullable=False)
	purchase_date = Column(Date, nullable=True)
	source = Column(String(256), nullable=True)
	manufacturer = Column(String(256), nullable=True)
	form = Column(Enum('seed', 'seedling', 'bulb', name='form'))


class Harvest(Base):
	__tablename__ = 'harvests'

	id = Column(Integer, primary_key=True)
	harvest_date = Column(Date)
	quantity = Column(Float)
	units = Column(String(128))
	notes = Column(String(512))
	next_year = Column(String(512))
	planting_id = Column(Integer, ForeignKey('plantings.id'))


class Group(Base):
	__tablename__ = 'groups'

	id = Column(Integer, primary_key=True)
	location = Column(String(256), nullable=False)