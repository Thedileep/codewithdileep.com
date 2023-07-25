document.addEventListener('DOMContentLoaded', function() {
    // Get references to the HTML elements
    const subjectSelect = document.getElementById('subject');
    const sessionYearSelect = document.getElementById('session_year');
    const studentsListDiv = document.getElementById('studentsList');

    // Event listener to handle changes in subject and session year select elements
    subjectSelect.addEventListener('change', populateStudentsList);
    sessionYearSelect.addEventListener('change', populateStudentsList);

    // Function to populate the students list
    function populateStudentsList() {
        const selectedSubjectId = subjectSelect.value;
        const selectedSessionYearId = sessionYearSelect.value;

        // Make a POST request to get the list of students
        fetch('/get_students/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                'subject': selectedSubjectId,
                'session_year': selectedSessionYearId
            })
        })
        .then(response => response.json())
        .then(data => {
            // Clear existing content
            studentsListDiv.innerHTML = '';

            // Populate the students list
            data.forEach(student => {
                const studentCheckbox = document.createElement('input');
                studentCheckbox.setAttribute('type', 'checkbox');
                studentCheckbox.setAttribute('name', 'student_ids');
                studentCheckbox.setAttribute('value', student.id);

                const studentLabel = document.createElement('label');
                studentLabel.textContent = student.name;

                const br = document.createElement('br');

                studentsListDiv.appendChild(studentCheckbox);
                studentsListDiv.appendChild(studentLabel);
                studentsListDiv.appendChild(br);
            });
        })
        .catch(error => {
            console.error('Error fetching students:', error);
        });
    }

    // Function to get the CSRF token for making POST requests
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Call the function initially to populate the students list
    populateStudentsList();
});
