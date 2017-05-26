from flask import request, jsonify, abort
from app import app, db
from app.common.db.tables import Job


@app.route('/', methods=['GET'])
def index():
    return "Kapivara Vagas"


@app.route('/jobs/', methods=['GET'])
def job_index():

    data = []
    jobs = Job.query.order_by(Job.date_pub.desc()).limit(5).all()
    for j in jobs:
        data.append({
            'id':j.id,
            "title":j.title,
            "location": j.location,
            "description":j.description,
            "email": j.email,
            "employment_contract": j.employment_contract,
            "modality": j.modality,
            "salary": float(j.salary),
            "website": j.website,
            "name_business": j.name_business,
            "url_job": j.url_job,
            "date_pub": j.date_pub
        })
    resp = jsonify(data)
    resp.status_code = 200
    resp.mimetype = 'application/json'
    resp.headers['Link'] = 'www.kapivara.top'
    return resp


@app.route('/job/<int:id>', methods=['GET'])
@app.route('/job/', methods=['POST'])
def jobs(id=None):
    if request.method == 'GET':
        data = []
        j = Job.query.filter_by(id=id).first()
        if j is not None:
            data.append({
                'id': j.id,
                "title": j.title,
                "location": j.location,
                "description": j.description,
                "email": j.email,
                "employment_contract": j.employment_contract,
                "modality": j.modality,
                "salary": float(j.salary),
                "website": j.website,
                "name_business": j.name_business,
                "url_job": j.url_job,
                "date_pub": j.date_pub
            })
            return jsonify(data)
        else:
            data = {}
            resp = jsonify(data)
            resp.status_code = 204
            resp.mimetype = 'application/json'
            resp.headers['Link'] = 'www.kapivara.top'
            return resp

    elif request.method == 'POST':

        if not request.json:
            abort(400)

        for r in ['title', 'email', 'location','description','name_business','website','salary','modality','employment_contract']:
            if r not in request.json:
                abort(400)

        new_job = Job(
            request.json['title'],
            request.json['description'],
            request.json['name_business'],
            request.json['location'],
            request.json['email'],
            request.json['website'],
            request.json['modality'],
            request.json['salary'],
            request.json['employment_contract'],
            request.json['url_job']
            )

        db.session.add(new_job)
        db.session.flush()
        db.session.commit()

        data = {
            'status': 200,
            'message':'Publication of Job success',
            'url': request.url + str(new_job.id)
        }

        return jsonify(data)


@app.route('/jobs/page/<int:num_page>', methods=['GET'])
def job_page(num_page=None):

    if num_page is 0:
        data = {
            'message':'Ei, Pe de Pano, da uma carimbada nesse cara.',
            'url': '/jobs/page/1'
        }
        return jsonify(data)
    else:
        data = []
        per_page = 10
        jobs = Job.query.order_by(Job.date_pub.desc()).paginate(page=num_page,per_page=5, error_out=False)
        for j in jobs.items:

            data.append({
                'id': j.id,
                "title": j.title,
                "location": j.location,
                "description": j.description,
                "email": j.email,
                "employment_contract": j.employment_contract,
                "modality": j.modality,
                "salary": float(j.salary),
                "website": j.website,
                "name_business": j.name_business,
                "url_job": j.url_job,
                "date_pub": j.date_pub
            })
        return jsonify(data)


@app.errorhandler(404)
def not_found(e):

    data = {
        'status': 404,
        'message': 'Not found: ' + request.url,
        'huehuebr':'"Um pra voce, um pra mim. Dois pra voce, um, dois pra mim.Tres pra voce, um, dois, tres pra mim..."'
    }
    resp = jsonify(data)
    resp.status_code = 404
    return resp


