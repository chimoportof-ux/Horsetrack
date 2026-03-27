document.addEventListener('DOMContentLoaded', () => {
  const messages = document.querySelectorAll('.message');
  if (messages.length) {
    setTimeout(() => {
      messages.forEach((msg) => {
        msg.style.opacity = '0';
        msg.style.transition = 'opacity 0.4s ease';
        setTimeout(() => msg.remove(), 400);
      });
    }, 3000);
  }
});
