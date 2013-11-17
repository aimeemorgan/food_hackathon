from flask import Flask, request, jsonify, abort, make_response
import model

app = Flask(__name__)


@app.teardown_appcontext
def shutdown_session(exception=None):
    model.session.remove()


@app.route('/garden/api/plantings', methods=['GET'])
def get_plantings():
    results = model.session.query(model.Planting).all()
    plantings = [{'id': d.id, 
                  'name': d.name,
                  'planted_date': serialize_date(d.planted_date),
                  'completed': d.completed,
                  'cultivar': d.cultivar_id,  
                  'group': d.group_id,             
                  'reminders': [f.id for f in d.reminders],
                  'harvests': [f.id for f in d.harvests]} 
                for d in results]
    return jsonify(plantings=plantings)


@app.route('/garden/api/plantings/<int:planting_id>', methods=['GET'])
def get_planting():
    result = model.session.query(model.Planting).get(planting_id)
    if result == None:
        abort(404)
    planting = {'id': result.id, 
                'name': result.name,
                'planted_date': serialize_date(result.planted_date),
                'completed': result.completed,
                'cultivar': result.cultivar_id,  
                'group': result.group_id,             
                'reminders': [f.id for f in result.reminders],
                'harvests': [f.id for f in result.harvests]}
    return jsonify(planting=planting)


@app.route('/garden/api/plantings', methods=['POST'])
def create_planting():
    if not request.json:
        abort(400)
    new_planting = model.Planting()
    if 'name' in request.json and type(request.json['name']) != str:
        abort(400)
    new_planting.name = request.json.get('name', '')
    planted_date_string = request.json.get('planted_date', '')
    new_planting.planted_date = deserialize_date(planted_date_string)
    new_planting.completed = False
    if ('cultivar_id' in request.json and 
        type(request.json['cultivar_id']) != int):
        abort(400)
    new_planting.cultivar_id = request.json.get('cultivar_id', '')
    if ('group_id' in request.json and 
        type(request.json['group_id']) != int):
        abort(400)
    new_planting.group_id = request.json.get('group_id', '')
    model.session.add(new_planting)
    model.session.commit()
    return 201


@app.route('/garden/api/plantings/<int:planting_id>', methods=['DELETE'])
def delete_planting(planting_id):
    planting = model.session.query(model.Planting).get(planting_id)
    if planting == None:
        abort(404)
    model.session.delete(planting)
    model.session.commit()
    return jsonify({'result': True})


@app.route('/garden/api/groups', methods=['GET'])
def get_groups():
    results = model.session.query(model.Group).all()
    groups = [{'id': d.id, 'location': d.location} for d in results]
    return jsonify(groups=groups)


@app.route('/garden/api/groups/<int:group_id>', methods=['GET'])
def get_group(group_id):
    group = model.session.query(model.Group).get(group_id)
    if group == None:
        abort(404)
    return jsonify(id=group.id, location=group.location)


@app.route('/garden/api/groups', methods=['POST'])
def create_group():
    if not request.json or 'location' not in request.json:
        abort(400)
    new_group = model.Group()
    if type(request.json['location']) != str:
        abort(400)
    new_group.location = request.json['location']
    model.session.add(new_group)
    model.session.commit()
    return 201


@app.route('/garden/api/groups/<int:group_id>', methods=['DELETE'])
def delete_group(group_id):
    group = model.session.query(model.Group).get(group_id)
    if group == None:
        abort(404)
    model.session.delete(group)
    model.session.commit()
    return jsonify({'result': True})


@app.route('/garden/api/reminders', methods=['GET'])
def get_reminders():
    results = model.session.query(model.Reminder).all()
    reminders_list = [{'id': d.id, 
                       'due_date': d.due_date,
                       'kind': d.kind,
                       'text': d.text,
                       'completed_date': serialize_date(d.completed_date),
                       'recurrence': d.recurrence,
                       'planting_id': d.planting_id} for d in results]
    return jsonify(reminders=reminders_list)


@app.route('/garden/api/reminders/<int:reminder_id>', methods=['GET'])
def get_reminder(reminder_id):
    reminder = model.session.query(model.Reminder).get(reminder_id)
    if reminder == None:
        abort(404)
    return jsonify(id=reminder.id,
                   due_date= due_date,
                   kind=reminder.kind,
                   text=reminder.text,
                   completed_date=reminder.completed_date,
                   recurrence=reminder.recurrence,
                   planting_id=reminder.planting_id)


@app.route('/garden/api/reminders/<int:reminder_id>', methods=['DELETE'])
def delete_reminder(reminder_id):
    reminder = model.session.query(model.Reminder).get(reminder_id)
    if reminder == None:
        abort(404)
    model.session.delete(reminder)
    model.session.commit()
    return jsonify({'result': True})


@app.route('/garden/api/cultivars', methods=['GET'])
def get_cultivars():
    results = model.session.query(model.Cultivar).all()
    cultivars = [{'id': d.id, 
                  'name': d.name,
                  'type': d.cultivar_type,
                  'purchase_date': serialize_date(d.purchase_date),
                  'manufacturer': d.manufacturer,
                  'source': d.source,
                  'form': d.form,
                  'days_to_harvest': d.days_to_harvest,
                  'plantings': [f.id for f in d.plantings]} 
                 for d in results]
    return jsonify(cultivars=cultivars)


@app.route('/garden/api/cultivar/<int:cultivar_id>', methods=['GET'])
def get_cultivar(cultivar_id):
    result = model.session.query(model.Cultivar).get(cultivar_id)
    if result == None:
        abort(404)
    cultivar = {'id': result.id, 
                'name': result.name,
                'type': result.cultivar_type,
                'purchase_date': serialize_date(result.purchase_date),
                'manufacturer': result.manufacturer,
                'source': result.source,
                'form': result.form,
                'days_to_harvest': result.days_to_harvest,
                'plantings': [f.id for f in result.plantings]} 
    return jsonify(cultivar=cultivar)


@app.route('/garden/api/cultivars/<int:cultivar_id>', methods=['DELETE'])
def delete_cultivar(cultivar_id):
    cultivar = model.session.query(model.Cultivar).get(cultivar_id)
    if cultivar == None:
        abort(404)
    model.session.delete(cultivar)
    model.session.commit()
    return jsonify({'result': True})


@app.route('/garden/api/harvests', methods=['GET'])
def get_harvests():
    results = model.session.query(model.Harvest).all()
    harvests = [{'id': d.id, 
                 'harvest_date': serialize_date(d.harvest_date),
                 'quantity': d.quantity,
                 'units': d.units,
                 'notes': d.notes,
                 'next_year': d.next_year,
                 'planting_id': d.planting_id} 
               for d in results]
    return jsonify(harvests=harvests)


@app.route('/garden/api/harvests/<int:harvest_id>', methods=['GET'])
def get_harvest(harvest_id):
    result = model.session.query(model.Harvest).get(harvest_id)
    if result == None:
        abort(404)
    harvest = {'id': result.id, 
               'harvest_date': serialize_date(result.harvest_date),
               'quantity': result.quantity,
               'units': result.units,
               'notes': result.notes,
               'next_year': result.next_year,
               'planting_id': result.planting_id} 
    return jsonify(harvest=harvest)   


@app.route('/garden/api/harvests/<int:harvest_id>', methods=['DELETE'])
def delete_harvest(harvest_id):
    harvest = model.session.query(model.Harvest).get(harvest_id)
    if harvest == None:
        abort(404)
    model.session.delete(harvest)
    model.session.commit()
    return jsonify({'result': True})


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)


@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify( { 'error': 'Bad request' } ), 400)


def serialize_date(date):
    if date == None:
        return None
    return '%i, %i, %i' % (date.year, date.month, date.day)


def deserialize_date(datestring):
    if not datestring:
        return None
    datelist = datestring.split("'")
    return Date(datelist[0], datelist[1], datelist[2])


if __name__ == '__main__':
    app.run(debug = True)