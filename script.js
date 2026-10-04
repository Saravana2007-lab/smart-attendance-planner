
 const operation = document.getElementById("operation");
const updateBox = document.getElementById("updateBox");


// =====================================================
// SHOW UPDATE FIELD ONLY FOR UPDATE ATTENDANCE
// =====================================================

operation.addEventListener("change", function () {

    if (operation.value === "update") {
        updateBox.classList.remove("hidden");
    } else {
        updateBox.classList.add("hidden");
    }

});


// =====================================================
// CLEAN AND NORMALIZE SUBJECT
// =====================================================

function cleanSubject(subject) {

    subject = subject.trim().replace(/\s+/g, " ").toLowerCase();

    const subjects = {

        "python": "Python",

        "operating system": "Operating System",

        "computer network": "Computer Network",

        "dbms": "DBMS",

        "web programming": "Web Programming"

    };

    return subjects[subject] || null;
}


// =====================================================
// MAIN FUNCTION
// =====================================================

async function performOperation() {

    const selectedOperation =
        document.getElementById("operation").value;

    const studentName =
        document.getElementById("studentName").value.trim();

    const rollNumber =
        document.getElementById("rollNumber").value;

    const subject =
        cleanSubject(
            document.getElementById("subject").value
        );

    const newClasses =
        document.getElementById("newClasses").value;


    // CHECK OPERATION

    if (selectedOperation === "") {

        alert("Please select an option.");

        return;
    }


    // CHECK NAME

    if (studentName === "") {

        alert("Please enter student name.");

        return;
    }


    // CHECK ROLL NUMBER

    if (rollNumber === "") {

        alert("Please enter roll number.");

        return;
    }


    // CHECK SUBJECT

    if (subject === null) {

        alert("Please enter a valid subject.");

        return;
    }


    // CHECK CLASSES FOR UPDATE

    if (
        selectedOperation === "update"
        &&
        (
            newClasses === ""
            ||
            Number(newClasses) <= 0
        )
    ) {

        alert("Please enter the number of classes to add.");

        return;
    }


    // =================================================
    // SEND DATA TO PYTHON FLASK
    // =================================================

    try {

        const response = await fetch(
            "/api/attendance",
            {

                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({

                    operation: selectedOperation,

                    studentName: studentName,

                    rollNumber: rollNumber,

                    subject: subject,

                    newClasses: newClasses

                })

            }
        );


        const data = await response.json();


        // PYTHON ERROR

        if (!data.success) {

            alert(data.message);

            return;
        }


        // DISPLAY DATABASE RESULT

        displayResult(data);

    }


    catch (error) {

        alert(
            "Could not connect to Python server."
        );

        console.log(error);

    }

}


// =====================================================
// DISPLAY RESULT
// =====================================================

function displayResult(data) {

    const resultCard =
        document.getElementById("resultCard");

    const result =
        document.getElementById("result");


    resultCard.classList.remove("hidden");


    // =================================================
    // UPDATE ATTENDANCE
    // =================================================

    if (data.operation === "update") {

        result.innerHTML = `

            <div class="result-box">

                <div class="result-row">

                    <span class="result-label">
                        Student Name
                    </span>

                    <span class="result-value">
                        ${data.studentName}
                    </span>

                </div>


                <div class="result-row">

                    <span class="result-label">
                        Roll Number
                    </span>

                    <span class="result-value">
                        ${data.rollNumber}
                    </span>

                </div>


                <div class="result-row">

                    <span class="result-label">
                        Subject
                    </span>

                    <span class="result-value">
                        ${data.subject}
                    </span>

                </div>


                <div class="result-row">

                    <span class="result-label">
                        Total Classes
                    </span>

                    <span class="result-value">
                        ${data.totalClasses}
                    </span>

                </div>


                <div class="result-row">

                    <span class="result-label">
                        Attended Classes
                    </span>

                    <span class="result-value">
                        ${data.attendedClasses}
                    </span>

                </div>


                <div class="result-row">

                    <span class="result-label">
                        Attendance
                    </span>

                    <span class="result-value">
                        ${data.attendance}%
                    </span>

                </div>

            </div>

        `;

        return;
    }


    // =================================================
    // VIEW ATTENDANCE
    // =================================================

    if (data.operation === "view") {

        result.innerHTML = `

            <div class="result-box">

                <div class="result-row">

                    <span class="result-label">
                        Student Name
                    </span>

                    <span class="result-value">
                        ${data.studentName}
                    </span>

                </div>


                <div class="result-row">

                    <span class="result-label">
                        Roll Number
                    </span>

                    <span class="result-value">
                        ${data.rollNumber}
                    </span>

                </div>


                <div class="result-row">

                    <span class="result-label">
                        Subject
                    </span>

                    <span class="result-value">
                        ${data.subject}
                    </span>

                </div>


                <div class="result-row">

                    <span class="result-label">
                        Total Classes
                    </span>

                    <span class="result-value">
                        ${data.totalClasses}
                    </span>

                </div>


                <div class="result-row">

                    <span class="result-label">
                        Attended Classes
                    </span>

                    <span class="result-value">
                        ${data.attendedClasses}
                    </span>

                </div>


                <div class="result-row">

                    <span class="result-label">
                        Attendance
                    </span>

                    <span class="result-value">
                        ${data.attendance}%
                    </span>

                </div>

            </div>

        `;

        return;
    }


    // =================================================
    // CALCULATE ATTENDANCE
    // =================================================

    if (data.operation === "calculate") {

        result.innerHTML = `

            <div class="result-box">

                <div class="result-row">

                    <span class="result-label">
                        Student Name
                    </span>

                    <span class="result-value">
                        ${data.studentName}
                    </span>

                </div>


                <div class="result-row">

                    <span class="result-label">
                        Roll Number
                    </span>

                    <span class="result-value">
                        ${data.rollNumber}
                    </span>

                </div>


                <div class="result-row">

                    <span class="result-label">
                        Subject
                    </span>

                    <span class="result-value">
                        ${data.subject}
                    </span>

                </div>


                <div class="result-row">

                    <span class="result-label">
                        Total Classes
                    </span>

                    <span class="result-value">
                        ${data.totalClasses}
                    </span>

                </div>


                <div class="result-row">

                    <span class="result-label">
                        Attended Classes
                    </span>

                    <span class="result-value">
                        ${data.attendedClasses}
                    </span>

                </div>


                <div class="result-row">

                    <span class="result-label">
                        Attendance
                    </span>

                    <span class="result-value">
                        ${data.attendance}%
                    </span>

                </div>

            </div>

        `;

        return;
    }


    // =================================================
    // CLASSES REQUIRED FOR 75%
    // =================================================

    if (data.operation === "required") {

        result.innerHTML = `

            <div class="result-box">

                <div class="result-row">

                    <span class="result-label">
                        Student Name
                    </span>

                    <span class="result-value">
                        ${data.studentName}
                    </span>

                </div>


                <div class="result-row">

                    <span class="result-label">
                        Roll Number
                    </span>

                    <span class="result-value">
                        ${data.rollNumber}
                    </span>

                </div>


                <div class="result-row">

                    <span class="result-label">
                        Subject
                    </span>

                    <span class="result-value">
                        ${data.subject}
                    </span>

                </div>


                <div class="result-row">

                    <span class="result-label">
                        Current Attendance
                    </span>

                    <span class="result-value">
                        ${data.attendance}%
                    </span>

                </div>


                <div class="result-row">

                    <span class="result-label">
                        Classes Required
                    </span>

                    <span class="result-value">
                        ${data.classesRequired}
                    </span>

                </div>

            </div>

        `;

        return;
    }


    // =================================================
    // CLASSES YOU CAN MISS
    // =================================================

    if (data.operation === "miss") {

        if (data.below75 === true) {

            result.innerHTML = `

                <div class="result-box">

                    <div class="result-row">

                        <span class="result-label">
                            Student Name
                        </span>

                        <span class="result-value">
                            ${data.studentName}
                        </span>

                    </div>


                    <div class="result-row">

                        <span class="result-label">
                            Roll Number
                        </span>

                        <span class="result-value">
                            ${data.rollNumber}
                        </span>

                    </div>


                    <div class="result-row">

                        <span class="result-label">
                            Subject
                        </span>

                        <span class="result-value">
                            ${data.subject}
                        </span>

                    </div>


                    <div class="result-row">

                        <span class="result-label">
                            Current Attendance
                        </span>

                        <span class="result-value">
                            ${data.attendance}%
                        </span>

                    </div>


                    <div class="result-row">

                        <span class="result-label">
                            Classes You Can Miss
                        </span>

                        <span class="result-value">
                            0
                        </span>

                    </div>


                    <div class="result-row">

                        <span class="result-label">
                            Classes Required for 75%
                        </span>

                        <span class="result-value">
                            ${data.classesRequired}
                        </span>

                    </div>

                </div>

            `;

        } else {

            result.innerHTML = `

                <div class="result-box">

                    <div class="result-row">

                        <span class="result-label">
                            Student Name
                        </span>

                        <span class="result-value">
                            ${data.studentName}
                        </span>

                    </div>


                    <div class="result-row">

                        <span class="result-label">
                            Roll Number
                        </span>

                        <span class="result-value">
                            ${data.rollNumber}
                        </span>

                    </div>


                    <div class="result-row">

                        <span class="result-label">
                            Subject
                        </span>

                        <span class="result-value">
                            ${data.subject}
                        </span>

                    </div>


                    <div class="result-row">

                        <span class="result-label">
                            Current Attendance
                        </span>

                        <span class="result-value">
                            ${data.attendance}%
                        </span>

                    </div>


                    <div class="result-row">

                        <span class="result-label">
                            Classes You Can Miss
                        </span>

                        <span class="result-value">
                            ${data.classesCanMiss}
                        </span>

                    </div>

                </div>

            `;

        }

        return;
    }


    // =================================================
    // ATTENDANCE REPORT
    // =================================================

    if (data.operation === "report") {

        let html = `<div class="result-box">`;


        data.report.forEach(function (student) {

            html += `

                <div class="result-row">

                    <span class="result-label">

                        ${student.studentName}
                        -
                        ${student.subject}

                    </span>


                    <span class="result-value">

                        ${student.attendance}%

                    </span>

                </div>

            `;

        });


        html += `</div>`;


        result.innerHTML = html;

    }

}
