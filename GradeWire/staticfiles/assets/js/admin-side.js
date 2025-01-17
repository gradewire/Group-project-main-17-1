function toggleSidebar() {
    const sidebar = document.querySelector('.sidebar');
    sidebar.classList.toggle('active');
}

function showSection(sectionId) {
    const sections = document.querySelectorAll('.section');
    sections.forEach(section => section.classList.remove('active'));

    const activeSection = document.getElementById(sectionId);
    if (activeSection) {
        activeSection.classList.add('active');
    }
}





function searchStudent() {
    const searchValue = document.getElementById('searchStudent').value.toLowerCase();
    const tableRows = document.getElementById('studentTableBody').querySelectorAll('tr');

    tableRows.forEach(row => {
        const name = row.cells[1].textContent.toLowerCase();
        const studentClass = row.cells[2].textContent.toLowerCase();

        if (name.includes(searchValue) || studentClass.includes(searchValue)) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    });
}




function searchTeacher() {
const searchValue = document.getElementById('searchTeacher').value.toLowerCase();
const tableRows = document.getElementById('teacherTableBody').querySelectorAll('tr');

tableRows.forEach(row => {
const name = row.cells[1].textContent.toLowerCase();
const subject = row.cells[2].textContent.toLowerCase();

if (name.includes(searchValue) || subject.includes(searchValue)) {
    row.style.display = '';
} else {
    row.style.display = 'none';
}
});
}



// Initializing the charts

const studentsCourseChartCtx = document.getElementById('studentsCourseChart').getContext('2d');
new Chart(studentsCourseChartCtx, {
    type: 'bar',
    data: {
        labels: ['Course 1', 'Course 2', 'Course 3', 'Course 4'],
        datasets: [{
            label: 'Number of Students',
            data: [30, 25, 40, 25],
            backgroundColor: '#1e90ff',
        }]
    }
});