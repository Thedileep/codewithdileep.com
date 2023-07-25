$(document).ready(function () {
    // Function to populate attendance dates based on selected subject and session year
    function getAttendanceDates() {
        var subjectId = $("#subject").val();
        var sessionYearId = $("#session_year").val();

        $.ajax({
            type: "POST",
            url: "/get_attendance_dates/",
            data: {
                subject: subjectId,
                session_year_id: sessionYearId,
                csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
            },
            success: function (data) {
                var options = '<option value="" selected disabled>Select Attendance Date</option>';
                for (var i = 0; i < data.length; i++) {
                    options +=
                        '<option value="' +
                        data[i].id +
                        '">' +
                        data[i].attendance_date +
                        "</option>";
                }
                $("#attendance_date").html(options);
            },
            error: function (error) {
                console.log(error);
            },
        });
    }

    // Function to get attendance details of selected date
    function getAttendanceDetails() {
        var attendanceDateId = $("#attendance_date").val();

        $.ajax({
            type: "POST",
            url: "/get_attendance_student/",
            data: {
                attendance_date: attendanceDateId,
                csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
            },
            success: function (data) {
                var details = "";
                for (var i = 0; i < data.length; i++) {
                    var status = data[i].status ? "Present" : "Absent";
                    details +=
                        "<tr><td>" +
                        data[i].name +
                        "</td><td>" +
                        status +
                        "</td></tr>";
                }
                $("#attendance_details").html(details);
            },
            error: function (error) {
                console.log(error);
            },
        });
    }

    // Event listener for subject and session year dropdowns
    $("#subject, #session_year").change(function () {
        getAttendanceDates();
    });

    // Event listener for attendance date dropdown
    $("#attendance_date").change(function () {
        getAttendanceDetails();
    });

    // Event listener for form submission
    $("#updateAttendanceForm").submit(function (event) {
        event.preventDefault();
        var form = $(this);

        $.ajax({
            type: "POST",
            url: "/update_attendance_data/",
            data: form.serialize(),
            success: function (response) {
                if (response === "OK") {
                    alert("Attendance updated successfully!");
                    form.trigger("reset");
                    $("#attendance_details").html("");
                } else {
                    alert("Error updating attendance!");
                }
            },
            error: function (error) {
                console.log(error);
                alert("Error updating attendance!");
            },
        });
    });
});
