from flask import jsonify, Blueprint, request
from flask.views import MethodView
from app import db, app
import json

bpInterest = Blueprint('bpInterest', __name__)


class Interest(MethodView):

    @staticmethod
    def get(id=None):
        res = {}

        query = f"select * from interest where interest_id = {id}"
        results = db.engine.execute(query)
        for result in results:
            res_data = {
                'interest_id': result.interest_id,
                'interest_name': result.interest_name,
                'created_date': result.created_date,
                'last_updated_date': result.last_updated_date
            }
            res['data'] = res_data

        filters = [
            {
                'column_name': 'interest_name',
                'type': 'text',
                'label': 'Interest Name'
            },
            {
                'column_name': 'created_date',
                'type': 'date',
                'label': 'Created Date From'
            },
            {
                'column_name': 'created_date',
                'type': 'date',
                'label': 'Created Date To'
            },
            {
                'column_name': 'last_updated_date',
                'type': 'date',
                'label': 'Last Updated Date From'
            },
            {
                'column_name': 'last_updated_date',
                'type': 'date',
                'label': 'Last Updated Date To'
            }
        ]
        res['filters'] = filters

        return jsonify(res)

    @staticmethod
    def post():
        offset = request.json.get('offset')
        limit = request.json.get('limit')
        filters = json.loads(request.json.get('filters'))

        res = {}

        filter_interest_name = ''
        filter_created_date = ''
        filter_last_updated_date = ''

        if not filters['interest_name']:
            filter_interest_name = f"and upper(interest_name) like " \
                                   f"upper(\'%{filters['interest_name']}%\')"
        
        if not filters['created_date_from'] and not filters['created_date_to']:
            filter_created_date = f"and created_date between {filters['created_date_from']} " \
                                  f"and {filters['created_date_to']}"

        if not filters['last_updated_date_from'] and not filters['last_updated_date_to']:
            filter_last_updated_date = f"and last_updated_date between {filters['last_updated_date_from']} " \
                                       f"and {filters['last_updated_date_to']}"

        query_data = f"select * from interest" \
                     f"where 1=1" \
                     f"{filter_interest_name}" \
                     f"{filter_created_date}" \
                     f"{filter_last_updated_date}" \
                     f"offset {offset} limit {limit}"
        data = db.engine.execute(query_data)

        res_data = []

        index = 0
        for result in data:
            data = {
                'interest_id': result.interest_id,
                'interest_name': result.interest_name,
                'created_date': result.created_date,
                'last_updated_date': result.last_updated_date
            }

            res_data.append(data)
            index += 1

        filters = [
            {
                'column_name': 'interest_name',
                'type': 'text',
                'label': 'Interest Name'
            },
            {
                'column_name': 'created_date_from',
                'type': 'date',
                'label': 'Created Date From'
            },
            {
                'column_name': 'created_date_to',
                'type': 'date',
                'label': 'Created Date To'
            },
            {
                'column_name': 'last_updated_date_from',
                'type': 'date',
                'label': 'Last Updated Date From'
            },
            {
                'column_name': 'last_updated_date_to',
                'type': 'date',
                'label': 'Last Updated Date To'
            }
        ]

        res['data'] = res_data
        res['filters'] = filters

        return jsonify(res)


interest = Interest.as_view('interest')
app.add_url_rule(
    '/interest/', view_func=interest, methods=['POST']
)
app.add_url_rule(
    '/interest/<int:id>', view_func=interest, methods=['GET']
)
