import json
from google.cloud import bigquery

def getUserInfo(request):
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

        client = bigquery.Client()

        # Query the database
        query = f"""
        WITH project_details AS (
            SELECT ARRAY_AGG(STRUCT(p.id, p.name)) AS projects
            FROM `cloud-and-advanced-analytics.CloudProject.ProjectUsers` AS pu
            INNER JOIN `cloud-and-advanced-analytics.CloudProject.Projects` AS p
            ON pu.projectId = p.id
            WHERE pu.userId = '{user_id}'
        ), event_details AS (
            SELECT MOD(COUNT(*), 2) = 1 AS working
            FROM `cloud-and-advanced-analytics.CloudProject.Events` 
            WHERE userId = '{user_id}'
        ), user_details AS (
            SELECT name
            FROM `cloud-and-advanced-analytics.CloudProject.Users`
            WHERE id = '{user_id}'
        )
        SELECT u.name, e.working, p.projects
        FROM user_details AS u
        CROSS JOIN event_details AS e
        CROSS JOIN project_details AS p;
        """

        query_job = client.query(query)
        result = query_job.result()

        # Extracting the data
        for row in result:
            output = {
                "name": row.name,
                "working": row.working,
                "projects": [dict(project) for project in row.projects]
            }

        return json.dumps(output), 200

    except Exception as e:
        error = {"error": str(e)}
        return json.dumps(error), 500
