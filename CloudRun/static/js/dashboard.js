$(document).ready(function () {
    // Get user status
    $.ajax({
        url: '/user_status',
        type: 'GET',
        success: function(data) {
            let userStatusDiv = $("#user-status");
            Object.keys(data).forEach(function(key) {
                // let statusCircle = "<span class='status-circle' style='background-color: " + (data[key] ? "green" : "red") + "'></span>";
                // userStatusDiv.append("<p>" + key + ": " + statusCircle + "</p>");
                // under each user, add a small circle with green or red color using a bar chart
                let graphcontainer = document.createElement('div');
                let pieCanvas = document.createElement('canvas');
                let progressText = document.createElement('p');
                
                userStatusDiv.append(graphcontainer);
                progressText.innerHTML = key + ": <br>" + data[key];
                graphcontainer.append(progressText);
                graphcontainer.append(pieCanvas);
                
                // fully green if data[key] is true, fully red if false
                let ctx = pieCanvas.getContext('2d');
                new Chart(ctx, {
                    type: 'pie',
                    data: {
                        datasets: [{
                            data: [data[key], 1 - data[key]],
                            backgroundColor: ["green", "grey"]
                        }],
                    }
                });
            });
        }
    });

    // Get user progress
    $.ajax({
        url: '/user_progress',
        type: 'GET',
        success: function(data) {
            let userProgressDiv = $("#user-progress");
            Object.keys(data).forEach(function(key) {
                let progress = data[key];
                let graphcontainer = document.createElement('div');
                let pieCanvas = document.createElement('canvas');
                let progressText = document.createElement('p');
                
                userProgressDiv.append(graphcontainer);
                progressText.innerHTML = key + ": <br>" + progress.text;
                graphcontainer.append(progressText);
                graphcontainer.append(pieCanvas);

                let ctx = pieCanvas.getContext('2d');
                new Chart(ctx, {
                    type: 'pie',
                    data: {
                        datasets: [{
                            data: [progress.hours, progress.objectiveHours - progress.hours],
                            backgroundColor: ["green", "grey"]
                        }],
                    }
                });
            });
        }
    });

    // Get project progress
    $.ajax({
        url: '/project_progress',
        type: 'GET',
        success: function(data) {
            let projectProgressDiv = $("#project-progress");
            Object.keys(data).forEach(function(key) {
                let progress = data[key];
                let graphcontainer = document.createElement('div');
                let pieCanvas = document.createElement('canvas');
                let progressText = document.createElement('p');
    
                projectProgressDiv.append(graphcontainer);
                progressText.innerHTML = key + ": <br>" + progress.text;
                graphcontainer.append(progressText);
                graphcontainer.append(pieCanvas);
    
                let ctx = pieCanvas.getContext('2d');
                new Chart(ctx, {
                    type: 'pie',
                    data: {
                        datasets: [{
                            data: [progress.hours, progress.objectiveHours - progress.hours],
                            backgroundColor: ["green", "grey"]
                        }],
                    }
                });
            });
        }
    });

    // Manage tables
    let usersTable = $("#users-table").DataTable();
    let projectsTable = $("#projects-table").DataTable();
    let projectUsersTable = $("#project-users-table").DataTable();

    // Get all users
    $.ajax({
        url: '/users',
        type: 'GET',
        success: function(data) {
            data.forEach(function(user) {
                usersTable.row.add([user.id, user.name, user.workHours]).draw();
            });
        }
    });

    // Get all projects
    $.ajax({
        url: '/projects',
        type: 'GET',
        success: function(data) {
            data.forEach(function(project) {
                projectsTable.row.add([project.id, project.name, project.projectHours]).draw();
            });
        }
    });

    // Get users in projects
    $.ajax({
        url: '/project_users',
        type: 'GET',
        success: function(data) {
            data.forEach(function(project) {
                // projectUsersTable.row.add([project.name, project.users]).draw();
                let users = project.users;
                let usersString = "";
                users.forEach(function(user) {
                    usersString += user + ", ";
                }
                );
                usersString = usersString.substring(0, usersString.length - 2);
                projectUsersTable.row.add([project.name, usersString]).draw();
            });
        }
    });

    // Add user
    $("#add-user-button").click(function() {
        let id = $("#user-id-input").val();
        let name = $("#user-name-input").val();
        let workHours = $("#user-work-hours-input").val();

        $.ajax({
            url: '/add_user',
            type: 'POST',
            contentType: "application/json",
            data: JSON.stringify({
                id: id,
                name: name,
                workHours: workHours
            }),
            success: function(data) {
                // usersTable.row.add([id, name, workHours]).draw();
                alert(data.message);
                location.reload();
            },
            error: function(xhr, status, error) {
                alert(error);
            }
        });
    });

    // Add project
    $("#add-project-button").click(function() {
        let id = $("#project-id-input").val();
        let name = $("#project-name-input").val();
        let projectHours = $("#project-hours-input").val();

        $.ajax({
            url: '/add_project',
            type: 'POST',
            contentType: "application/json",
            data: JSON.stringify({
                id: id,
                name: name,
                projectHours: projectHours
            }),
            success: function(data) {
                // projectsTable.row.add([id, name, projectHours]).draw();
                alert(data.message);
                location.reload();
            },
            error: function(xhr, status, error) {
                alert(error);
            }
        });
    });

    // Assign user to project
    $("#assign-user-button").click(function() {
        let projectId = $("#project-id-assign-input").val();
        let userId = $("#user-id-assign-input").val();

        $.ajax({
            url: '/add_user_to_project',
            type: 'POST',
            contentType: "application/json",
            data: JSON.stringify({
                projectId: projectId,
                userId: userId
            }),
            success: function(data) {
                alert(data.message);
                location.reload();
            },
            error: function(xhr, status, error) {
                alert(error);
            }
        });
    });
});
