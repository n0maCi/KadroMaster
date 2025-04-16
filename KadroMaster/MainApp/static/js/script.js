document.getElementById('pageSelect').addEventListener('change', function() {
    var selectedPage = this.value;
    if (selectedPage) {
        window.location.href = selectedPage;
    }
});
