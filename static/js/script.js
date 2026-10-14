// Auto-dismiss flash alerts after a few seconds for a cleaner UX.
document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".alert").forEach((alertEl) => {
    setTimeout(() => {
      const alert = bootstrap.Alert.getOrCreateInstance(alertEl);
      alert.close();
    }, 6000);
  });
});
