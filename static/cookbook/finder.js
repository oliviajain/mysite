// Ingredient finder: sends the ticked ingredients to the server and lists the closest recipes.
(function () {
  const form = document.getElementById('finder');
  const out = document.getElementById('finder-results');
  if (!form || !out) return;

  form.addEventListener('submit', async function (event) {
    event.preventDefault();
    const selected = Array.from(form.querySelectorAll('input[type="checkbox"]:checked')).map(function (box) { return box.value; });
    out.textContent = 'Looking…';

    try {
      const response = await fetch(form.dataset.endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ selectedOptions: selected })
      });
      if (!response.ok) throw new Error('Request failed: ' + response.status);
      render(await response.json());
    } catch (error) {
      console.error(error);
      out.textContent = 'Something went wrong. Please try again.';
    }
  });

  function render(data) {
    out.textContent = '';
    const heading = document.createElement('h2');
    heading.textContent = 'Closest matches';
    heading.style.marginTop = '0';
    out.appendChild(heading);

    // Fewest missing ingredients first.
    Object.keys(data)
      .sort(function (a, b) { return data[a].length - data[b].length || a.localeCompare(b); })
      .forEach(function (name) {
        const missing = data[name];
        const row = document.createElement('div');
        row.className = 'result';

        const link = document.createElement('a');
        link.href = form.dataset.recipeUrl.replace('__name__', encodeURIComponent(name));
        link.textContent = name;

        const note = document.createElement('p');
        note.textContent = missing.length > 0 ? 'Missing: ' + missing.join(', ') : 'You have everything :)';

        row.appendChild(link);
        row.appendChild(note);
        out.appendChild(row);
      });

    out.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }
})();
