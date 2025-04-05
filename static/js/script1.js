document.addEventListener('DOMContentLoaded', () => {
    const buttons = document.querySelectorAll('.button');
    if (buttons.length > 0) {
        buttons.forEach(button => {
            button.addEventListener('click', function() {
                alert('More details coming soon!');
            });
        });
    }
});
