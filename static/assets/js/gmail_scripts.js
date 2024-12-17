function rotateIcon() {
    var icon = document.getElementById('refresh-icon');
    icon.classList.add('rotate');
    
    // Optional: If you want to stop the rotation after the data is refreshed
    document.addEventListener('htmx:afterSwap', function() {
        icon.classList.remove('rotate');
    });
}