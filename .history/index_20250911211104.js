// ------------------- NAVBAR -------------------
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

// ------------------- FORM SUBMISSION -------------------
async function predictAdoption(event) {
    event.preventDefault();

    // Get form values
    const petData = {
        PetType: document.getElementById("PetType").value,
        Breed: document.getElementById("Breed").value,
        AgeMonths: parseInt(document.getElementById("AgeMonths").value),
        Color: document.getElementById("Color").value || "Unknown",
        Size: document.getElementById("Size").value,
        WeightKg: parseFloat(document.getElementById("WeightKg").value),
        Vaccinated: document.getElementById("Vaccinated").value,
        HealthCondition: document.getElementById("HealthCondition").value,
        TimeInShelterDays: parseInt(document.getElementById("TimeInShelterDays").value),
        AdoptionFee: parseFloat(document.getElementById("AdoptionFee").value),
        PreviousOwner: document.getElementById("PreviousOwner").value
    };

    try {
        const response = await fetch("http://127.0.0.1:8000/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(petData)
        });

        if (!response.ok) {
            throw new Error(`Server error: ${response.status}`);
        }

        const result = await response.json();

        document.getElementById("result").innerText =
            result.prediction === 1
                ? "✅ This pet is likely to be adopted!"
                : "❌ Low adoption likelihood.";
    } catch (error) {
        document.getElementById("result").innerText = "⚠️ Error connecting to API.";
        console.error("API Error:", error);
    }
}

// Attach event listener to your form
document.getElementById("adoptionForm").addEventListener("submit", predictAdoption);
