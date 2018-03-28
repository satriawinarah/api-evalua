
from flask import jsonify, Blueprint
from flask.views import MethodView
from app import db, app

bpTableColumnLength = Blueprint('bpTableColumnLength', __name__)


class TableColumnLength(MethodView):

    def get(self, tableCode:''):
        queryColumn = f"select column_name, column_length, column_data_type from table_column where table_code = '{tableCode}' order by column_order asc"
        columns = db.engine.execute(queryColumn)
        resColumn = []
        for result in columns:
            column = {
                'column_name': result.column_name,
                'column_length': result.column_length,
                'column_data_type': result.column_data_type
            }
            resColumn.append(column)

        queryLength = f"select count(*) as length from {tableCode}"
        length = db.engine.execute(queryLength)
        resLength = 0
        for result in length:
            resLength = result.length

        res = {}
        res['column'] = resColumn
        res['table_length'] = resLength

        return jsonify(res)


tablecolumnlength = TableColumnLength.as_view('tablecolumnlength')
app.add_url_rule(
    '/column-length/<string:tableCode>', view_func=tablecolumnlength, methods=['GET']
)
