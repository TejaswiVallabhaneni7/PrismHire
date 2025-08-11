// static/js/app.js
document.getElementById('uploadForm').addEventListener('submit', async function(e){
  e.preventDefault();
  const job = document.getElementById('job').value;
  const resume = document.getElementById('resume').files[0];
  if (!resume) { alert("Please choose a resume file."); return; }
  const formData = new FormData();
  formData.append('job', job);
  formData.append('resume', resume);

  document.getElementById('submitBtn').disabled = true;
  document.getElementById('submitBtn').innerText = "Analyzing...";

  try {
    const resp = await fetch('/upload', { method: 'POST', body: formData });
    if (!resp.ok){
      const err = await resp.json();
      alert("Error: " + (err.error || JSON.stringify(err)));
      throw new Error("Upload failed");
    }
    const data = await resp.json();
    showResults(data);
  } catch (err){
    console.error(err);
  } finally {
    document.getElementById('submitBtn').disabled = false;
    document.getElementById('submitBtn').innerText = "Analyze resume";
  }
});

function showResults(data){
  document.getElementById('results').style.display = 'block';
  const score = Math.round(data.score * 100);
  document.getElementById('scoreVal').innerText = score + "% match";
  document.getElementById('overlap').innerText = `${data.match_percent_keywords}% keywords matched`;
  const mk = document.getElementById('matchedKeywords');
  mk.innerHTML = "";
  (data.matched_keywords || []).forEach(k => {
    const span = document.createElement('span');
    span.className = 'chip';
    span.innerText = k;
    mk.appendChild(span);
  });
  document.getElementById('snippet').innerText = data.text_snippet || '';

  // draw donut chart
  const ctx = document.getElementById('scoreChart').getContext('2d');
  if (window._prismChart) {
    window._prismChart.data.datasets[0].data = [score, 100-score];
    window._prismChart.update();
  } else {
    window._prismChart = new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: ['Match','Remaining'],
        datasets: [{
          data: [score, 100-score],
          backgroundColor: ['#00d4ff', '#1f2b3a'],
          borderWidth: 0
        }]
      },
      options: {
        cutout: '75%',
        plugins: {
          legend: { display: false }
        }
      }
    });
  }
}
