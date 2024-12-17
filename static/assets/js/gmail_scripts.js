function rotateIcon(event) {
    var button = event.target.closest('button'); 
    console.log('Button clicked:', button);

    var icon = button.querySelector('.icon_rotation');
    if (icon) {
        icon.classList.add('rotate');
    }

    document.addEventListener('htmx:afterSwap', function() {
        if (icon) {
            icon.classList.remove('rotate');
        }
    });
}