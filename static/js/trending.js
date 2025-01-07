buttons = document.querySelectorAll('.list-group-item');
sections = document.querySelectorAll('section');
sections.forEach((section, index) => {
    if (index != 0) {
        section.style.display = 'none';
    }
});
buttons.forEach((button, index) => {
    if (index == 0) {
        button.classList.add('active');
    }
});
buttons.forEach((button, index) => {
    button.addEventListener('click', () => {
        sections.forEach((section, i) => {
            if (index == i) {
                section.style.display = 'block';
                button.classList.add('active');
            } else {
                section.style.display = 'none';
                buttons[i].classList.remove('active');
            }
        });
    });
});