/* Honour-board table filter (ported from the static history pages). */
function filterTable(filter, btn) {
  document.querySelectorAll('.hb-filter-btn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  const rows = document.querySelectorAll('#honours-table tbody tr');
  rows.forEach(row => {
    if (filter === 'all') {
      row.style.display = '';
    } else if (filter === 'recent') {
      row.style.display = (row.dataset.era === 'recent' || row.classList.contains('covid')) ? '' : 'none';
    } else if (filter === 'pl') {
      row.style.display = (row.dataset.grade === 'pl') ? '' : 'none';
    }
  });
}
