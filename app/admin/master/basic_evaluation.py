from flask import jsonify, Blueprint
from flask.views import MethodView
from app import db, app

bpBasicEvaluation = Blueprint('bpBasicEvaluation', __name__)


@bpBasicEvaluation.route('/basic-evaluation/columns')
def basicEvaluationColumns():
    query = """
    select column_name from information_schema.columns where table_name = 'basic_evaluation' and table_schema = 'public'
    """
    columns = db.engine.execute(query)
    res = []
    for column in columns:
        res.append(column.column_name)
    return jsonify(res)


class BasicEvaluation(MethodView):

    def get(self, id=None, page=1):
        if not id:
            results = db.engine.execute('select * from basic_evaluation')
            res = {}
            for result in results:
                res[result.evaluation_id] = {
                    'evaluationName': result.evaluation_name,
                    'evaluationDescription': result.evaluation_description,
                    'evaluationPoint': result.evaluation_point,
                    'evaluationTypeValue': result.evaluation_type_value,
                    'evaluationPeriod': result.evaluation_period,
                    'createdDate': result.created_date,
                    'lastUpdatedDate': result.last_updated_date
                }
        else:
            query = f"select * from basic_evaluation where evaluation_id = {id}"
            results = db.engine.execute(query)
            res = {}
            for result in results:
                res = {
                    'evaluationId': result.evaluation_id,
                    'evaluationName': result.evaluation_name,
                    'evaluationDescription': result.evaluation_description,
                    'evaluationPoint': result.evaluation_point,
                    'evaluationTypeValue': result.evaluation_type_value,
                    'evaluationPeriod': result.evaluation_period,
                    'createdDate': result.created_date,
                    'lastUpdatedDate': result.last_updated_date
                }

        return jsonify(res)


basicEvaluation = BasicEvaluation.as_view('basic_evaluation')
app.add_url_rule(
    '/basic-evaluation/', view_func=basicEvaluation, methods=['GET', 'POST']
)
app.add_url_rule(
    '/basic-evaluation/<int:id>', view_func=basicEvaluation, methods=['GET']
)
