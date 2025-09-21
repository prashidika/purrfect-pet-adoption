// NAVBAR
const navbar = document.querySelector("nav");

// Scroll effect
window.addEventListener("scroll", () =>
    navbar.classList.toggle("sticky", window.scrollY > 0)
);

// Menu toggle
const menu = document.querySelector(".menu");
const toggleMenu = () => menu.classList.toggle("active");

// Event listeners for open/close menu
document.querySelector(".menu-btn").addEventListener("click", toggleMenu);
document.querySelector(".close-btn").addEventListener("click", toggleMenu);

// Close menu when clicking a link
document
    .querySelectorAll(".menu a")
    .forEach((link) => link.addEventListener("click", toggleMenu));
