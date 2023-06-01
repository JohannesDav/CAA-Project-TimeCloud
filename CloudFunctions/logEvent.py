import json
from google.cloud import bigquery
from datetime import datetime

def logEvent(request):
    """HTTPS Cloud Function.
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    """
    try:
        data = request.get_json(force=True)
        user_id = data['userId']
        project_id = data['projectId']

        client = bigquery.Client()

        # Insert the event
        table_id = "cloud-and-advanced-analytics.CloudProject.Events"
        table = client.get_table(table_id)  # Make an API request.
        current_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        rows_to_insert = [(user_id, current_time, project_id)]

        errors = client.insert_rows(table, rows_to_insert)  # Make an API request.
        if errors == []:
            print("New rows have been added.")
            return json.dumps({"message": "Event logged successfully"}), 200
        else:
            print("Encountered errors while inserting rows: {}".format(errors))
            return json.dumps({"error": str(errors)}), 500

    except Exception as e:
        error = {"error": str(e)}
        return json.dumps(error), 500
