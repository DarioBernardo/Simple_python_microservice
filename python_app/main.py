from flask import Flask
from flask import jsonify
from flask import make_response
from flask import request
import datetime as dt
from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import file_html

from TimeSeriesModel import TimeSeriesModel

app = Flask("MircoserviceAPI", static_folder="./static")

model = TimeSeriesModel()

HTTP_ERROR_CLIENT = 422
HTTP_ERROR_SERVER = 500
HTTP_OK = 200


@app.route('/', methods=['GET'])
def index():

    return app.send_static_file('index.html')


@app.route('/visualize', methods=['GET'])
def visualize_account_api():

    if 'account_no' not in request.args or request.args['account_no'] in ("", None):
        return make_response(jsonify({'error': 'parameter account_no not is missing'}), HTTP_ERROR_CLIENT)

    try:
        account_no = int(request.args.get('account_no', ''))
    except Exception as e:
        return make_response(jsonify({'error': "ERR_INVALID_TYPE:  %s" % e},
                                     HTTP_ERROR_CLIENT))

    df = model.get_data_for_accout(account_no)

    p = figure(width=1400, height=800, x_axis_type="datetime")
    p.line(df['date'], df['cleared_balance'], color='navy', alpha=0.5, legend='Cleared Balance')
    p.line(df['date'], df['ewm'], color='red', alpha=0.5, legend="Exponential Weighted Mean")
    p.line(df['date'], df['ma'], color='green', alpha=0.5, legend=" Moving averate (35 days window)")

    html = file_html(p, CDN, "Plot for account %s" % account_no)
    return html


@app.route('/add', methods=['GET'])
def add_data_to_account_no_api():

    if 'account_no' not in request.args or request.args['account_no'] in ("", None):
        return make_response(jsonify({'error': 'parameter account_no not is missing'}), HTTP_ERROR_CLIENT)

    if 'date' not in request.args or request.args['date'] in ("", None):
        return make_response(jsonify({'error': 'parameter date is missing'}), HTTP_ERROR_CLIENT)

    if 'ledger_balance' not in request.args or request.args['ledger_balance'] in ("", None):
        return make_response(jsonify({'error': 'parameter ledger_balance is missing'}), HTTP_ERROR_CLIENT)

    if 'cleared_balance' not in request.args or request.args['cleared_balance'] in ("", None):
        return make_response(jsonify({'error': 'parameter cleared_balance is missing'}), HTTP_ERROR_CLIENT)

    try:
        account_no = int(request.args.get('account_no', ''))
        ledger_balance = float(request.args.get('ledger_balance', ''))
        cleared_balance = float(request.args.get('cleared_balance', ''))
        date = dt.datetime.strptime(request.args.get('date', ''), '%Y-%m-%d')
    except Exception as e:
        return make_response(jsonify({'error': "ERR_INVALID_TYPE:  %s" % e}),
                                     HTTP_ERROR_CLIENT)

    if account_no < 0:
        return make_response(jsonify({'error': "ERR_OUT_OF_BOUNDS:  'account_no' parameger must be a postitive integer"}),
                                     HTTP_ERROR_CLIENT)

    message_type = model.add_point_to_ts(account_no, date, ledger_balance, cleared_balance)

    try:
        return make_response(jsonify({'ID_CODE':'%s' % message_type}), HTTP_OK)
    except Exception as ex:
        return make_response(jsonify({'error': ex}), HTTP_ERROR_SERVER)

if __name__ == '__main__':
    app.run()
