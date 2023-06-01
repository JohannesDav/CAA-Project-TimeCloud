import os
import json
from flask import Flask, request, jsonify, render_template
from google.cloud import bigquery

app = Flask(__name__)

# for local testing only
# PATH_TO_CREDENTIALS_FILE = "/home/johannes/timbreuse/cloud-and-advanced-analytics-9366c3817771.json"
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = PATH_TO_CREDENTIALS_FILE

client = bigquery.Client()

@app.route("/")
def dashboard():
    return render_template("dashboard.html")

@app.route('/user_status')
def get_user_status(): # are the users currently working?
    query = """
    SELECT u.id AS user_id, u.name AS user_name, MOD(COUNT(e.userId), 2) = 1 AS status
    FROM `cloud-and-advanced-analytics.CloudProject.Users` AS u
    LEFT JOIN `cloud-and-advanced-analytics.CloudProject.Events` AS e
    ON u.id = e.userId
    GROUP BY u.id, u.name
    """
    query_job = client.query(query)
    result = query_job.result()

    output = {}
    for row in result:
        #output[row.user_id] = row.status
        output[row.user_name] = row.status
    return jsonify(output)

@app.route('/user_progress') # how much time did the users spend working?
def get_user_progress():
    query = """
    SELECT u.id AS user_id, u.name AS user_name, e.logTime AS log_time, e.projectId AS project_id
    FROM `cloud-and-advanced-analytics.CloudProject.Users` AS u
    LEFT JOIN `cloud-and-advanced-analytics.CloudProject.Events` AS e
    ON u.id = e.userId
    ORDER BY u.id, e.logTime
    """

    query_job = client.query(query)
    result = query_job.result()

    user_times = {}
    current_user = None
    start_time = {}

    for row in result:
        if row.user_id != current_user:
            current_user = row.user_id
            start_time[current_user] = None
            user_times[current_user] = 0

        if row.project_id != "default-stop" and start_time[current_user] is None:
            start_time[current_user] = row.log_time
        elif row.project_id == "default-stop" and current_user and start_time[current_user] is not None:
            time_difference = row.log_time - start_time[current_user]
            user_times[current_user] += time_difference.total_seconds() / 3600 # convert to hours
            start_time[current_user] = None

    user_query = f"""
    SELECT id, name, workHours
    FROM `cloud-and-advanced-analytics.CloudProject.Users`
    """
    user_query_job = client.query(user_query)
    user_result = user_query_job.result()
    user_result = list(user_result)

    progress = {}
    for user_id, total_hours in user_times.items():
        for row in user_result:
            if row.id == user_id:
                work_hours = row.workHours
                # progress[row.name] = "{:.2f} hours / {:.2f} hours".format(total_hours, work_hours)
                progress[row.name] = {"text": "{:.2f} / {:.2f} hours".format(total_hours, work_hours), "ratio": total_hours / work_hours, "hours": total_hours, "objectiveHours": work_hours}
                break
        # no progress so far
        if row.name not in progress:
            work_hours = row.workHours
            progress[row.name] = {"text": "{:.2f} / {:.2f} hours".format(0, work_hours), "ratio": 0, "hours": 0, "objectiveHours": work_hours}

    return jsonify(progress)


@app.route('/project_progress')
def get_project_progress(): # how much time was spent on each project?
    query = """
    SELECT u.id AS user_id, u.name AS user_name, e.logTime AS log_time, e.projectId AS project_id
    FROM `cloud-and-advanced-analytics.CloudProject.Users` AS u
    LEFT JOIN `cloud-and-advanced-analytics.CloudProject.Events` AS e
    ON u.id = e.userId
    ORDER BY u.id, e.logTime
    """

    query_job = client.query(query)
    result = query_job.result()

    project_times = {}
    current_user = None
    current_project = None
    start_time = {}

    for row in result:
        if row.user_id != current_user:
            current_user = row.user_id
            start_time[current_user] = None
        if row.project_id not in project_times:
            project_times[row.project_id] = 0

        if row.project_id != "default-stop" and start_time[current_user] is None:
            start_time[current_user] = row.log_time
            current_project = row.project_id
        elif row.project_id == "default-stop" and current_user and start_time[current_user] is not None:
            time_difference = row.log_time - start_time[current_user]
            project_times[current_project] += time_difference.total_seconds() / 3600 # convert to hours
            start_time[current_user] = None

    project_query = f"""
    SELECT id, name, projectHours
    FROM `cloud-and-advanced-analytics.CloudProject.Projects`
    """
    project_query_job = client.query(project_query)
    project_result = project_query_job.result()
    project_result = list(project_result)

    progress = {}
    for row in project_result:
        for project_id, total_hours in project_times.items():
            if row.id == project_id:
                project_hours = row.projectHours
                # progress[row.name] = "{:.2f} hours / {:.2f} hours".format(total_hours, project_hours)
                progress[row.name] = {"text": "{:.2f} / {:.2f} hours".format(total_hours, project_hours), "ratio": total_hours / project_hours, "hours": total_hours, "objectiveHours": project_hours}
                break
        # no progress so far
        if row.name not in progress:
            project_hours = row.projectHours
            progress[row.name] = {"text": "{:.2f} / {:.2f} hours".format(0, project_hours), "ratio": 0, "hours": 0, "objectiveHours": project_hours}

    return jsonify(progress)


@app.route('/users')
def get_all_users():
    query = """
    SELECT id AS user_id, name AS user_name, workHours AS work_hours
    FROM `cloud-and-advanced-analytics.CloudProject.Users`
    """
    query_job = client.query(query)
    result = query_job.result()

    output = []
    for row in result:
        output.append({
            "id": row.user_id,
            "name": row.user_name,
            "workHours": row.work_hours
        })
    return jsonify(output)

@app.route('/projects')
def get_all_projects():
    query = """
    SELECT id AS project_id, name AS project_name, projectHours AS project_hours
    FROM `cloud-and-advanced-analytics.CloudProject.Projects`
    """
    query_job = client.query(query)
    result = query_job.result()

    output = []
    for row in result:
        output.append({
            "id": row.project_id,
            "name": row.project_name,
            "projectHours": row.project_hours
        })
    return jsonify(output)

@app.route('/project_users', methods=['GET'])
def get_users_in_projects(): # for each project list of the users that are assigned to it
    query = f"""
    SELECT u.id AS user_id, u.name AS user_name, p.id AS project_id, p.name AS project_name
    FROM `cloud-and-advanced-analytics.CloudProject.Users` AS u
    LEFT JOIN `cloud-and-advanced-analytics.CloudProject.ProjectUsers` AS pu
    ON u.id = pu.userId
    LEFT JOIN `cloud-and-advanced-analytics.CloudProject.Projects` AS p
    ON pu.projectId = p.id
    """
    query_job = client.query(query)
    result = query_job.result()

    output = {}
    for row in result:
        if row.project_id not in output:
            output[row.project_id] = {
                "name": row.project_name,
                "users": []
            }
        output[row.project_id]["users"].append(row.user_name)
    
    output = list(output.values())
    output = [item for item in output if item["name"] is not None]

    return jsonify(output)

@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.get_json()
    user_id = data['id']
    name = data['name']
    work_hours = data['workHours']

    query = f"""
    INSERT `cloud-and-advanced-analytics.CloudProject.Users` (id, name, workHours)
    VALUES ('{user_id}', '{name}', {work_hours});
    """
    query_job = client.query(query)
    return jsonify({"message": "User added successfully"}), 200

@app.route('/add_project', methods=['POST'])
def add_project():
    data = request.get_json()
    project_id = data['id']
    name = data['name']
    project_hours = data['projectHours']

    query = f"""
    INSERT `cloud-and-advanced-analytics.CloudProject.Projects` (id, name, projectHours)
    VALUES ('{project_id}', '{name}', {project_hours});
    """
    query_job = client.query(query)
    return jsonify({"message": "Project added successfully"}), 200

@app.route('/add_user_to_project', methods=['POST'])
def add_user_to_project():
    data = request.get_json()
    user_id = data['userId']
    project_id = data['projectId']

    query = f"""
    INSERT `cloud-and-advanced-analytics.CloudProject.ProjectUsers` (userId, projectId)
    VALUES ('{user_id}', '{project_id}');
    """
    query_job = client.query(query)
    return jsonify({"message": "User added to project successfully"}), 200


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080))) 
