from flask import jsonify, Blueprint
from flask.views import MethodView
from app import db, app

bpAdminHistory = Blueprint('bpAdminHistory', __name__)


@bpAdminHistory.route('/admin-history/columns')
def adminHistoryColumns():
    query = """
    select column_name from information_schema.columns where table_name = 'admin_history' and table_schema = 'public'
    """
    columns = db.engine.execute(query)
    res = []
    for column in columns:
        res.append(column.column_name)
    return jsonify(res)


class AdminHistory(MethodView):

    def get(self, id=None, page=1):
        if not id:
            results = db.engine.execute('select * from admin_history')
            res = {}
            for result in results:
                res[result.admin_history_id] = {
                    'adminId': result.admin_id,
                    'action': result.action,
                    'actionDate': result.action_date
                }
        else:
            query = f"select * from admin_history where admin_history_id = {id}"
            results = db.engine.execute(query)
            res = {}
            for result in results:
                res = {
                    'adminHistoryId': result.admin_history_id,
                    'adminId': result.admin_id,
                    'action': result.action,
                    'actionDate': result.action_date
                }

        return jsonify(res)


adminHistory = AdminHistory.as_view('admin_history')
app.add_url_rule(
    '/admin-history/', view_func=adminHistory, methods=['GET', 'POST']
)
app.add_url_rule(
    '/admin-history/<int:id>', view_func=adminHistory, methods=['GET']
)