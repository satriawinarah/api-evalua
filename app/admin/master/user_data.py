from flask import jsonify, Blueprint
from flask.views import MethodView
from app import db, app

bpUserData = Blueprint('bpUserData', __name__)


@bpUserData.route('/user/columns')
def userDataColumns():
    query = """
    select column_name from information_schema.columns where table_name = 'user_data' and table_schema = 'public'
    """
    columns = db.engine.execute(query)
    res = []
    for column in columns:
        res.append(column.column_name)
    return jsonify(res)


class UserData(MethodView):

    def get(self, id=None, page=1):
        if not id:
            results = db.engine.execute('select * from user_data')
            res = {}
            for result in results:
                res[result.user_id] = {
                    'userEmail': result.user_email,
                    'userFullName': result.user_full_name,
                    'userPassword': result.user_password,
                    'userAddress': result.user_address,
                    'userCountry': result.user_country,
                    'userGender': result.user_gender,
                    'userProfilePicture': result.user_profile_picture,
                    'createdDate': result.created_date,
                    'lastUpdatedDate': result.last_updated_date
                }
        else:
            query = f"select * from user_data where user_id = {id}"
            results = db.engine.execute(query)
            res = {}
            for result in results:
                res = {
                    'userId': result.user_id,
                    'userEmail': result.user_email,
                    'userFullName': result.user_full_name,
                    'userPassword': result.user_password,
                    'userAddress': result.user_address,
                    'userCountry': result.user_country,
                    'userGender': result.user_gender,
                    'userProfilePicture': result.user_profile_picture,
                    'createdDate': result.created_date,
                    'lastUpdatedDate': result.last_updated_date
                }

        return jsonify(res)


userData = UserData.as_view('user_data')
app.add_url_rule(
    '/user/', view_func=userData, methods=['GET', 'POST']
)
app.add_url_rule(
    '/user/<int:id>', view_func=userData, methods=['GET']
)
