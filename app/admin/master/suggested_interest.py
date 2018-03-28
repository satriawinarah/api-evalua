from flask import jsonify, Blueprint
from flask.views import MethodView
from app import db, app

bpSuggestedInterest = Blueprint('bpSuggestedInterest', __name__)


@bpSuggestedInterest.route('/suggested-interest/columns')
def suggestedInterestColumns():
    query = """
    select column_name from information_schema.columns where table_name = 'suggested_interest' and table_schema = 'public'
    """
    columns = db.engine.execute(query)
    res = []
    for column in columns:
        res.append(column.column_name)
    return jsonify(res)


class SuggestedInterest(MethodView):

    def get(self, id=None, page=1):
        if not id:
            results = db.engine.execute('select * from suggested_interest')
            res = {}
            for result in results:
                res[result.suggested_interest_id] = {
                    'suggestedInterestName': result.suggested_interest_name,
                    'isValidInterest': result.is_valid_interest,
                    'isUsedInterest': result.is_used_interest,
                    'createdDate': result.created_date,
                    'lastUpdatedDate': result.last_updated_date
                }
        else:
            query = f"select * from suggested_interest where suggested_interest_id = {id}"
            results = db.engine.execute(query)
            res = {}
            for result in results:
                res = {
                    'suggestedInterestId': result.suggested_interest_id,
                    'suggestedInterestName': result.suggested_interest_name,
                    'isValidInterest': result.is_valid_interest,
                    'isUsedInterest': result.is_used_interest,
                    'createdDate': result.created_date,
                    'lastUpdatedDate': result.last_updated_date
                }

        return jsonify(res)


suggestedInterest = SuggestedInterest.as_view('suggested_interest')
app.add_url_rule(
    '/suggested-interest/', view_func=suggestedInterest, methods=['GET', 'POST']
)
app.add_url_rule(
    '/suggested-interest/<int:id>', view_func=suggestedInterest, methods=['GET']
)
