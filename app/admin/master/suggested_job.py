from flask import jsonify, Blueprint
from flask.views import MethodView
from app import db, app

bpSuggestedJob = Blueprint('bpSuggestedJob', __name__)


@bpSuggestedJob.route('/suggested-job/columns')
def suggestedJobColumns():
    query = """
    select column_name from information_schema.columns where table_name = 'suggested_job' and table_schema = 'public'
    """
    columns = db.engine.execute(query)
    res = []
    for column in columns:
        res.append(column.column_name)
    return jsonify(res)


class SuggestedJob(MethodView):

    def get(self, id=None, page=1):
        if not id:
            results = db.engine.execute('select * from suggested_job')
            res = {}
            for result in results:
                res[result.suggested_job_id] = {
                    'suggestedJobName': result.suggested_job_name,
                    'isValidInterest': result.is_valid_interest,
                    'isUsedInterest': result.is_used_interest,
                    'createdDate': result.created_date,
                    'lastUpdatedDate': result.last_updated_date
                }
        else:
            query = f"select * from suggested_job where suggested_job_id = {id}"
            results = db.engine.execute(query)
            res = {}
            for result in results:
                res = {
                    'suggestedJobId': result.suggested_job_id,
                    'suggestedJobName': result.suggested_job_name,
                    'isValidInterest': result.is_valid_interest,
                    'isUsedInterest': result.is_used_interest,
                    'createdDate': result.created_date,
                    'lastUpdatedDate': result.last_updated_date
                }

        return jsonify(res)


suggestedJob = SuggestedJob.as_view('suggested_job')
app.add_url_rule(
    '/suggested-job/', view_func=suggestedJob, methods=['GET', 'POST']
)
app.add_url_rule(
    '/suggested-job/<int:id>', view_func=suggestedJob, methods=['GET']
)
