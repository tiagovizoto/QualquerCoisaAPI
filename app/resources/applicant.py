from flask import request, jsonify,abort
from app import app, db
from app.common.db.tables import Job, Applicant


@app.route('/applicant/', methods=['POST'])
def applicante_send():

    if not request.json:
        abort(400)

    for r in ['name','email','id_job']:
        if r not in request.json:
            abort(400)

    data = {
        'name': request.json['name'],
        'email': request.json['email'],
        'message': request.json['message'],
        'id_job': request.json['id_job'],
    }

    if Job.query.filter_by(id=data['id_job']).first():
        try:
            applic = Applicant(data['name'],data['email'],data['id_job'],data['message'])
            db.session.add(applic)
            db.session.commit()
            resp = {
                'message':'Success Applicant'
            }
            return jsonify(resp), 200
        except Exception as e:
            return e
    else:
        resp = {
            'message': 'Job not found'
        }
        return jsonify(resp), 400