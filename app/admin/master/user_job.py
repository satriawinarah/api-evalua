from flask import jsonify, Blueprint
from flask.views import MethodView
from app import db, app

bpUserJob = Blueprint('bpUserJob', __name__)


@bpUserJob.route('/user-job/columns')
def userJobColumns():
    query = """
    select column_name from information_schema.columns where table_name = 'user_job' and table_schema = 'public'
    """
    columns = db.engine.execute(query)
    res = []
    for column in columns:
        res.append(column.column_name)
    return jsonify(res)


class UserJob(MethodView):

    def get(self, id=None, page=1):
        if not id:
            results = db.engine.execute('select * from user_job')
            res = {}
            for result in results:
                res[result.user_job_id] = {
                    'userId': result.user_id,
                    'jobId': result.job_id,
                    'jobPlace': result.job_place,
                    'createdDate': result.created_date,
                    'lastUpdatedDate': result.last_updated_date
                }
        else:
            query = f"select * from user_job where user_job_id = {id}"
            results = db.engine.execute(query)
            res = {}
            for result in results:
                res = {
                    'userJobId': result.user_job_id,
                    'userId': result.user_id,
                    'jobId': result.jobId,
                    'jobPlace': result.job_place,
                    'createdDate': result.created_date,
                    'lastUpdatedDate': result.last_updated_date
                }

        return jsonify(res)


userJob = UserJob.as_view('user_job')
app.add_url_rule(
    '/user-job/', view_func=userJob, methods=['GET', 'POST']
)
app.add_url_rule(
    '/user-job/<int:id>', view_func=userJob, methods=['GET']
)
