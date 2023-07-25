$(document).ready(function () {
    $("#viewAttendanceForm").submit(function (event) {
        event.preventDefault();
        var form = $(this);

        // Get selected subject and session year
        var subjectId = $("#subject").val();
        var sessionYearId = $("#session_year").val();

        // Send AJAX request to fetch attendance details
        $.ajax({
            type: "POST",
            url: "/get_attendance_details/",
            data: {
                subject_id: subjectId,
                session_year_id: sessionYearId,
                csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
            },
            success: function (data) {
                var attendanceDetails = $("#attendanceDetails");
                attendanceDetails.empty();

                if (data.length > 0) {
                    var table = $('<table class="table table-bordered"></table>');
                    var thead = $('<thead><tr><th>Student Name</th><th>Attendance Status</th></tr></thead>');
                    table.append(thead);

                    var tbody = $('<tbody></tbody>');
                    for (var i = 0; i < data.length; i++) {
                        var row = $('<tr></tr>');
                        row.append('<td>' + data[i].student_name + '</td>');
                        row.append('<td>' + data[i].attendance_status + '</td>');
                        tbody.append(row);
                    }
                    table.append(tbody);
                    attendanceDetails.append(table);
                } else {
                    attendanceDetails.text("No attendance data available for the selected subject and session year.");
                }
            },
            error: function (error) {
                console.log(error);
                alert("Error fetching attendance details!");
            },
        });
    });
});
