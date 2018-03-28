from flask import jsonify, Blueprint
from flask.views import MethodView
from app import db, app

bpJob = Blueprint('bpJob', __name__)


@bpJob.route('/job/columns')
def jobColumns():
    query = """
    select column_name from information_schema.columns where table_name = 'job' and table_schema = 'public'
    """
    columns = db.engine.execute(query)
    res = []
    for column in columns:
        res.append(column.column_name)
    return jsonify(res)


class Job(MethodView):

    def get(self, id=None, page=1):
        if not id:
            results = db.engine.execute('select * from job')
            res = {}
            for result in results:
                res[result.job_id] = {
                    'jobName': result.job_name,
                    'jobDescription': result.job_description,
                    'createdDate': result.created_date,
                    'lastUpdatedDate': result.last_updated_date
                }
        else:
            query = f"select * from job where job_id = {id}"
            results = db.engine.execute(query)
            res = {}
            for result in results:
                res = {
                    'jobId': result.job_id,
                    'jobName': result.job_name,
                    'jobDescription': result.job_description,
                    'createdDate': result.created_date,
                    'lastUpdatedDate': result.last_updated_date
                }

        return jsonify(res)


job = Job.as_view('job')
app.add_url_rule(
    '/job/', view_func=job, methods=['GET', 'POST']
)
app.add_url_rule(
    '/job/<int:id>', view_func=job, methods=['GET']
)
