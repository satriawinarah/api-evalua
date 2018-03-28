from flask import jsonify, Blueprint
from flask.views import MethodView
from app import db, app

bpAdmin = Blueprint('bpAdmin', __name__)


@bpAdmin.route('/admin/columns')
def adminColumns():
    query = """
    select column_name from information_schema.columns where table_name = 'admin' and table_schema = 'public'
    """
    columns = db.engine.execute(query)
    res = []
    for column in columns:
        res.append(column.column_name)
    return jsonify(res)


class Admin(MethodView):

    def get(self, id=None, page=1):
        if not id:
            results = db.engine.execute('select * from admin')
            res = {}
            for result in results:
                res[result.admin_id] = {
                    'name': result.admin_name,
                    'email': result.admin_email,
                    'password': result.admin_password,
                    'createdDate': result.created_date,
                    'lastUpdatedDate': result.last_updated_date
                }
        else:
            query = f"select * from admin where admin_id = {id}"
            results = db.engine.execute(query)
            res = {}
            for result in results:
                res = {
                    'name': result.admin_name,
                    'email': result.admin_email,
                    'password': result.admin_password,
                    'createdDate': result.created_date,
                    'lastUpdatedDate': result.last_updated_date
                }

        return jsonify(res)


admin = Admin.as_view('admin')
app.add_url_rule(
    '/admin/', view_func=admin, methods=['GET', 'POST']
)
app.add_url_rule(
    '/admin/<int:id>', view_func=admin, methods=['GET']
)
