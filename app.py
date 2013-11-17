from flask import Flask, render_template, redirect, request, jsonify
import model

app = Flask(__name__)


@app.teardown_appcontext
def shutdown_session(exception=None):
    model.session.remove()


# @app.route('/')
# def index():
# 	pass

# @app.route('/garden/api/plantings', methods=['GET'])
# def get_plantings():
# 	plantings = model.session.query(model.Planting).all()
# 	return jsonify(plantings)

@app.route('/garden/api/groups', methods=['GET'])
def get_groups():
	results = model.session.query(model.Group).all()
	groups_list = [{'id': d.id, 'location': d.location} for d in results]
	return jsonify(groups = groups_list)


@app.route('/garden/api/group/<int:group_id>', methods=['GET'])
def get_group(group_id):
	group = model.session.query(model.Group).get(group_id)
	return jsonify(id=group.id, location=group.location)


@app.route('/garden/api/reminders', methods=['GET'])
def get_reminders():
	results = model.session.query(model.Reminder).all()
	reminders_list = [{'id': d.id, 
					   'due_date': serialize_date(d.due_date),
					   'kind': d.kind,
					   'text': d.text,
					   'completed_date': serialize_date(d.completed_date),
					   'recurrence': d.recurrence,
					   'planting_id': d.planting_id} for d in results]
	return jsonify(reminders = reminders_list)


@app.route('/garden/api/reminder/<int:reminder_id>', methods=['GET'])
def get_reminder(reminder_id):
	reminder = model.session.query(model.Reminder).get(reminder_id)
	due_date = serialize_date(reminder.due_date)
	return jsonify(id=reminder.id,
				   due_date= due_date,
				   kind=reminder.kind,
				   text=reminder.text,
				   completed_date=reminder.completed_date,
				   recurrence=reminder.recurrence,
				   planting_id=reminder.planting_id)


# app.route('/garden/api/cultivars', methods=['GET'])
# def get_cultivars():
# 	results = model.session.query(model.Cultivars).all()
# 	cultivars_list = [{'id': d.id, 
# 					   'due_date': d.due_date,
# 					   'kind': d.kind,
# 					   'text': d.text,
# 					   'completed': d.completed,
# 					   'recurrence': d.recurrence,
# 					   'planting_id': d.planting_id} for d in results]
# 	return jsonify(cultivars = cultivars_list)


# @app.route('/garden/api/cultivars/<int:cultivar_id>', methods=['GET'])
# def get_cultivar(reminder_id):
# 	reminder = model.session.query(model.Reminder).get(reminder_id)
# 	return jsonify(id=reminder.id,
# 				   due_date= reminder.due_date,
# 				   kind=reminder.kind,
# 				   text=reminder.text,
# 				   completed=reminder.completed,
# 				   recurrence=reminder.recurrence,
# 				   planting_id=reminder.planting_id)


def serialize_date(date):
	if date == None:
		return None
	return '%i, %i, %i' % (date.year, date.month, date.day)


if __name__ == '__main__':
    app.run(debug = True)