const chartData = {
  labels: ['Mean', 'Median', 'Mode', 'Variance', 'SD'],
  datasets: [{
    label: 'Example Statistics',
    data: [20, 22, 19, 12, 4]
  }]
};

// Animate Introduction when it scrolls into view
document.addEventListener('DOMContentLoaded', () => {
  const intro = document.getElementById('introduction');
  if (!intro) return;

  // use IntersectionObserver so animations trigger when visible
  const obs = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        intro.classList.add('animate');
        observer.unobserve(intro);
      }
    });
  }, { threshold: 0.15 });

  obs.observe(intro);
});