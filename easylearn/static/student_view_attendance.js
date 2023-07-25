$(document).ready(function () {
    // Function to get attendance details based on selected subject
    function getAttendanceDetails() {
        var subjectId = $("#subject").val();

        $.ajax({
            type: "POST",
            url: "/get_student_attendance/",
            data: {
                subject: subjectId,
                csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
            },
            success: function (data) {
                var table = '<table>';
                table += '<tr><th>Attendance Date</th><th>Status</th></tr>';
                for (var i = 0; i < data.length; i++) {
                    var status = data[i].status ? "Present" : "Absent";
                    table += '<tr><td>' + data[i].attendance_date + '</td><td>' + status + '</td></tr>';
                }
                table += '</table>';
                $("#attendanceDetails").html(table);
            },
            error: function (error) {
                console.log(error);
            },
        });
    }

    // Event listener for form submission
    $("#viewAttendanceForm").submit(function (event) {
        event.preventDefault();
        getAttendanceDetails();
    });
});
