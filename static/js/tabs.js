// static/js/tabs.js

window.switchTab = function (name) {
  document
    .querySelectorAll(".tab")
    .forEach((t) => t.classList.remove("active"));
  document
    .querySelectorAll(".panel")
    .forEach((p) => p.classList.remove("active"));
  document
    .querySelectorAll(".sidebar a")
    .forEach((a) => a.classList.remove("active"));

  document.querySelector(`.tab[data-panel="${name}"]`).classList.add("active");
  document.getElementById(`panel-${name}`).classList.add("active");
  document
    .querySelector(`.sidebar a[data-tab="${name}"]`)
    .classList.add("active");
};

window.toggleTheme = function () {
  document.body.classList.toggle("dark");
  localStorage.setItem(
    "theme",
    document.body.classList.contains("dark") ? "dark" : "light"
  );
};

document.addEventListener("DOMContentLoaded", () => {
  if (localStorage.getItem("theme") === "dark") {
    document.body.classList.add("dark");
  }
});
