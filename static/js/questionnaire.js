prev = document.querySelectorAll('.previous');
next = document.querySelectorAll('.next');
progress = document.querySelector('.progress-bar');

sections = document.querySelectorAll('section');
sections[0].style.display = 'block';
sections[1].style.display = 'none';
sections[2].style.display = 'none';
sections[3].style.display = 'none';
sections[4].style.display = 'none';
i = 0;
prev.forEach(function (element) {
    element.addEventListener('click', function () {
        if (i > 0) {
            sections[i].style.display = 'none';
            i--;
            sections[i].style.display = 'block';
            progress.style.width = (i * 25) + '%';
            progress.innerHTML = (i * 25) + '%';
        }
    });
});
next.forEach(function (element) {
    element.addEventListener('click', function () {
        if (i < sections.length - 1) {
            sections[i].style.display = 'none';
            i++;
            sections[i].style.display = 'block';
            progress.style.width = (i * 25) + '%';
            progress.innerHTML = (i * 25) + '%';
        }
    });
});