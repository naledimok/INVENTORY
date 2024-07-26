// static/js/script.js

document.addEventListener("DOMContentLoaded", function() {
    // Initialize DataTables
    $(document).ready(function() {
        $('.inventory-table').DataTable();
    });

    // Add click event listener to table rows
    const rows = document.querySelectorAll("table tr");
    rows.forEach(row => {
        row.addEventListener("click", function() {
            alert(`You clicked on row with item: ${this.children[1].innerText}`);
        });
    });
});
