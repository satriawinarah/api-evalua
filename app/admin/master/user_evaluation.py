from flask import jsonify, Blueprint
from flask.views import MethodView
from app import db, app

bpUserEvaluation = Blueprint('bpUserEvaluation', __name__)


@bpUserEvaluation.route('/user-evaluation/columns')
def userEvaluationColumns():
    query = """
    select column_name from information_schema.columns where table_name = 'user_evaluation' and table_schema = 'public'
    """
    columns = db.engine.execute(query)
    res = []
    for column in columns:
        res.append(column.column_name)
    return jsonify(res)


class UserEvaluation(MethodView):

    def get(self, id=None, page=1):
        if not id:
            results = db.engine.execute('select * from user_evaluation')
            res = {}
            for result in results:
                res[result.user_evaluation_id] = {
                    'userId': result.user_id,
                    'evaluationId': result.evaluation_id,
                    'userEvaluationValue': result.user_evaluation_value,
                    'userCalculatedEvaluationValue': result.user_calculated_evaluation_value,
                    'userEvaluationPeriod': result.user_evaluation_period,
                    'createdDate': result.created_date,
                    'lastUpdatedDate': result.last_updated_date
                }
        else:
            query = f"select * from user_data where user_id = {id}"
            results = db.engine.execute(query)
            res = {}
            for result in results:
                res = {
                    'userEvaluationId': result.user_evaluation_id,
                    'userId': result.user_id,
                    'evaluationId': result.evaluation_id,
                    'userEvaluationValue': result.user_evaluation_value,
                    'userCalculatedEvaluationValue': result.user_calculated_evaluation_value,
                    'userEvaluationPeriod': result.user_evaluation_period,
                    'createdDate': result.created_date,
                    'lastUpdatedDate': result.last_updated_date
                }

        return jsonify(res)


userEvaluation = UserEvaluation.as_view('user_evaluation')
app.add_url_rule(
    '/user-evaluation/', view_func=userEvaluation, methods=['GET', 'POST']
)
app.add_url_rule(
    '/user-evaluation/<int:id>', view_func=userEvaluation, methods=['GET']
)
