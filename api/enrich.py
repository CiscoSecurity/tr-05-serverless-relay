from crayons import blue, green, white, red, yellow,magenta, cyan
from functools import partial
from api.schemas import ObservableSchema
from api.utils import get_json,get_jwt, jsonify_data, jsonify_errors, format_docs
from crayons import blue, green, white, red, yellow,magenta, cyan
from datetime import datetime, timedelta
from flask import Blueprint, current_app, jsonify, g
import requests

# FUNCTIONS

def group_observables(relay_input):
    # Leave only unique observables ( deduplicate observable )  and select some specific observable type
    result = []
    for observable in relay_input:
        o_value = observable['value']
        o_type = observable['type'].lower()

        # Get only supported types by this third party
        if o_type in current_app.config['CCT_OBSERVABLE_TYPES']:
            obj = {'type': o_type, 'value': o_value}
            if obj in result:
                continue
            result.append(obj)
    return result


def build_input_api(observables):
    # formating, cleanup
    for observable in observables:
        o_value = observable['value']
        o_type = observable['type'].lower()
        if current_app.config['CCT_OBSERVABLE_TYPES'][o_type].get('sep'):
            o_value = o_value.split(
                current_app.config['CCT_OBSERVABLE_TYPES'][o_type]['sep'])[-1]
            observable['value'] = o_value
    return observables


def call_api(value,api_key):
    # Send Call to Umbrella Investigate
    headers = {
'Authorization': 'Bearer ' + api_key
}
    response = requests.get(
        f"{current_app.config['API_URL']}"
        f"{current_app.config['API_PATH'].format(observable=value)}",
        headers=headers
    )

    return response.json()


def get_disposition(res):
    # Return tuple with (disposition, disposition_name)
    status=2 # just in case that res is empty.  then we will return disposition = unknown
    for keys,values in res.items():
        status=values['status']
        print(yellow(f"status = {status}",bold=True))
    if status==-1:
        return current_app.config['DISPOSITIONS']['malicious']
    elif status==0:
        return current_app.config['DISPOSITIONS']['clean']
    else:
        return current_app.config['DISPOSITIONS']['unknown']


def get_verdict(observable_value, observable_type,disposition, valid_time):
    '''
        Format the observable disposition into the CTIM format
    '''
    if disposition[0]==1:
        disposition_name='Clean'
    elif disposition[0]==2:
        disposition_name='Malicious'
    elif disposition[0]==3:
        disposition_name='Suspicious'
    elif disposition[0]==4:
        disposition_name='Common'
    elif disposition[0]==5:
        disposition_name='Unknown'
    else:
        disposition_name='Unknown'
    return {
        'type': 'verdict',
        'observable': {'type': observable_type, 'value': observable_value},
        'disposition': disposition[0],
        'disposition_name': disposition_name,
        'valid_time': valid_time
    }


enrich_api = Blueprint('enrich', __name__)

get_observables = partial(get_json, schema=ObservableSchema(many=True))

# ROUTES

@enrich_api.route('/deliberate/observables', methods=['POST'])
def deliberate_observables():
    api_key = get_jwt()  # Let's get the third party API Key
    data = {}  # Let's create a data directory to be sent back to Threat Response
    g.verdicts = []  # Let's create a list into which we will store valid verdicts data results for every observables
    relay_input = get_json(ObservableSchema(many=True))
    observables = group_observables(relay_input)
    if not observables:
        return jsonify_data({})
    observables = build_input_api(observables)
    for observable in observables:
        o_value = observable['value']
        o_type = observable['type'].lower()
        # print single observable for which to send a reputation query to the third party
        print(green(o_value, bold=True))
        disposition = call_api(o_value, api_key)
        # query the third party for the observable
        print(cyan(disposition, bold=True))

        # translate the third party returned value to Threat Response Expected value
        disposition_tuple = get_disposition(disposition)
        print(cyan(disposition_tuple, bold=True))

        # disposition_tuple is not empty then continue
        if not disposition_tuple:
            continue

        # disposition_tuple  then get the current date and calculate end date as an end of life date for judgment and verdicts
        # We need these information as mandatory information to return to Threat Response
        start_time = datetime.utcnow()
        end_time = start_time + timedelta(weeks=1)
        valid_time = {
            'start_time': start_time.isoformat() + 'Z',
            'end_time': end_time.isoformat() + 'Z',
        }
        # Let's append a new verdict item into the verdicts list with the minimum of information expected by the CTIM format
        g.verdicts.append(get_verdict(o_value, o_type, disposition_tuple, valid_time))

        # The g.verdicts list content all verdicts for every requested observable.  Let's add this list into the data dictionnary and do some formatting stuffs
    if g.verdicts:
        data['verdicts'] = format_docs(g.verdicts)

    # Let's get ready to send back a valid CTIM JSON result to the original Threat Response request . Let's put it into the result dictionnary
    result = {'data': data}
    print(green(f"JSON result to be sent to Threat Response : \n{result}", bold=True))
    return jsonify(result)


@enrich_api.route('/observe/observables', methods=['POST'])
def observe_observables():
    _ = get_jwt()
    _ = get_observables()
    return jsonify_data({})


@enrich_api.route('/refer/observables', methods=['POST'])
def refer_observables():
    _ = get_jwt()
    _ = get_observables()
    return jsonify_data([])
