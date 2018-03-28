from flask import jsonify, Blueprint
from flask.views import MethodView
from app import db, app

bpUserInterest = Blueprint('bpUserInterest', __name__)


@bpUserInterest.route('/user-interest/columns')
def userInterestColumns():
    query = """
    select column_name from information_schema.columns where table_name = 'user_interest' and table_schema = 'public'
    """
    columns = db.engine.execute(query)
    res = []
    for column in columns:
        res.append(column.column_name)
    return jsonify(res)


class UserInterest(MethodView):

    def get(self, id=None, page=1):
        if not id:
            results = db.engine.execute('select * from user_interest')
            res = {}
            for result in results:
                res[result.user_interest_id] = {
                    'userId': result.user_id,
                    'evaluationId': result.interest_id,
                    'createdDate': result.created_date,
                    'lastUpdatedDate': result.last_updated_date
                }
        else:
            query = f"select * from user_interest where user_id = {id}"
            results = db.engine.execute(query)
            res = {}
            for result in results:
                res = {
                    'userInterestId': result.user_interest_id,
                    'userId': result.user_id,
                    'evaluationId': result.interest_id,
                    'createdDate': result.created_date,
                    'lastUpdatedDate': result.last_updated_date
                }

        return jsonify(res)


userInterest = UserInterest.as_view('user_interest')
app.add_url_rule(
    '/user-interest/', view_func=userInterest, methods=['GET', 'POST']
)
app.add_url_rule(
    '/user-interest/<int:id>', view_func=userInterest, methods=['GET']
)
