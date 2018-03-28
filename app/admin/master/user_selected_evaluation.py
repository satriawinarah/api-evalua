from flask import jsonify, Blueprint
from flask.views import MethodView
from app import db, app

bpUserSelectedEvaluation = Blueprint('bpUserSelectedEvaluation', __name__)


@bpUserSelectedEvaluation.route('/user-selected-evaluation/columns')
def userSelectedEvaluation():
    query = """
    select column_name from information_schema.columns where table_name = 'user_selected_evaluation' and table_schema = 'public'
    """
    columns = db.engine.execute(query)
    res = []
    for column in columns:
        res.append(column.column_name)
    return jsonify(res)


class UserSelectedEvaluation(MethodView):

    def get(self, id=None, page=1):
        if not id:
            results = db.engine.execute('select * from user_selected_evaluation')
            res = {}
            for result in results:
                res[result.user_selected_evaluation_id] = {
                    'evaluationId': result.evaluation_id,
                    'userId': result.user_id,
                    'createdDate': result.created_date,
                    'lastUpdatedDate': result.last_updated_date
                }
        else:
            query = f"select * from user_selected_evaluation where user_selected_evaluation_id = {id}"
            results = db.engine.execute(query)
            res = {}
            for result in results:
                res = {
                    'userSelectedEvaluationId': result.user_selected_evaluation_id,
                    'evaluationId': result.evaluation_id,
                    'userId': result.user_id,
                    'createdDate': result.created_date,
                    'lastUpdatedDate': result.last_updated_date
                }

        return jsonify(res)


userSelectedEvaluation = UserSelectedEvaluation.as_view('user_selected_evaluation_id')
app.add_url_rule(
    '/user-selected-evaluation/', view_func=userSelectedEvaluation, methods=['GET', 'POST']
)
app.add_url_rule(
    '/user-selected-evaluation/<int:id>', view_func=userSelectedEvaluation, methods=['GET']
)
