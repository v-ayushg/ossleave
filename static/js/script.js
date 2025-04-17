document.addEventListener('DOMContentLoaded', function () {
    let calendarEl = document.getElementById('calendar');
    let calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        events: '/get_leaves'
    });
    calendar.render();

    document.getElementById('leave-form').addEventListener('submit', async function (e) {
        e.preventDefault();
        const form = e.target;
        const formData = new FormData(form);
        const name = formData.get('name');
        const date = formData.get('dates');

        await fetch('/add_leave', {
            method: 'POST',
            body: new URLSearchParams({
                'name': name,
                'dates[]': date
            })
        });

        alert("Leave marked successfully!");
        location.reload();
    });
});
