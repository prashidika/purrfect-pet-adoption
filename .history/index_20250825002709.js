// NAVBAR
const navbar = document.querySelector("nav");

// Fixed typo: 'window.scrolly' → 'window.scrollY' (capital Y)
window.addEventListener("scroll", () =>
    navbar.classList.toggle("sticky", window.scrollY > 0)
);

// Menu toggle for mobile
const menu = document.querySelector(".menu");
const toggleMenu = () => menu.classList.toggle("active");

// Add event listeners to open/close menu
document.querySelector(".menu-btn").addEventListener("click", toggleMenu);
document.querySelector(".close-btn").addEventListener("click", toggleMenu);

// Close menu when clicking on any link
document
    .querySelectorAll(".menu a")
    .forEach((link) => link.addEventListener("click", toggleMenu));
