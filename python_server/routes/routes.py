from flask import Blueprint, request, jsonify, render_template
from services import service

try:
    service_instance = service.Service()
except AttributeError:
     print("Warning: service.Service() instantiation pattern might need adjustment.")
     service_instance = service

case_routes = Blueprint('case_routes', __name__, template_folder='templates')

class CaseDTO:
    def __init__(self, case_id, subject, body):
        self.case_id = case_id
        self.subject = subject
        self.body = body

    def to_dict(self):
        return {
            'case_id': self.case_id,
            'subject': self.subject,
            'body': self.body
        }

@case_routes.route('/get_resolution', methods=['POST'])
def get_resolution():
    print("Received request for resolution")
    if not request.is_json:
        print("ERROR: Request body is not JSON")
        error_msg = "Request body must be JSON"
        return render_template('resolution_display.html', error=error_msg, case=None), 400

    data = request.get_json()
    case_id = data.get('case_id')
    subject = data.get('subject')
    body = data.get('body')

    if not all([case_id, subject, body]):
        missing = [k for k, v in {'case_id': case_id, 'subject': subject, 'body': body}.items() if not v]
        error_msg = f"Missing required fields: {', '.join(missing)}"
        partial_case_data = {'case_id': case_id, 'subject': subject, 'body': body}
        print(f"ERROR: one of the required fields is missing: {missing}")
        return render_template('resolution_display.html', error=error_msg, case=partial_case_data), 400

    case = CaseDTO(case_id, subject, body)
    case_data_for_template = case.to_dict()

    try:
        resolution = service_instance.get_resolution(case)
        return render_template('resolution_display.html', resolution=resolution, case=case_data_for_template), 200
    except Exception as e:
        print(f"Error processing case {case_id}: {e}")
        error_msg = f"An internal error occurred: {str(e)}"
        return render_template('resolution_display.html', error=error_msg, case=case_data_for_template), 500

# This route is for testing purposes and returns the raw resolution without rendering a template. 
@case_routes.route('/get_raw_resolution', methods=['POST'])
def get_raw_resolution():
    if not request.is_json:
        error_msg = "Request body must be JSON"
        return render_template('resolution_display.html', error=error_msg, case=None), 400

    data = request.get_json()
    case_id = data.get('case_id')
    subject = data.get('subject')
    body = data.get('body')

    if not all([case_id, subject, body]):
        missing = [k for k, v in {'case_id': case_id, 'subject': subject, 'body': body}.items() if not v]
        error_msg = f"Missing required fields: {', '.join(missing)}"
        partial_case_data = {'case_id': case_id, 'subject': subject, 'body': body}
        return render_template('resolution_display.html', error=error_msg, case=partial_case_data), 400

    case = CaseDTO(case_id, subject, body)
    case_data_for_template = case.to_dict()

    try:
        resolution = service_instance.get_resolution(case)
        return resolution, 200
    except Exception as e:
        print(f"Error processing case {case_id}: {e}")
        error_msg = f"An internal error occurred: {str(e)}"
        return render_template('resolution_display.html', error=error_msg, case=case_data_for_template), 500
    



   