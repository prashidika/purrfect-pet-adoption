// NAVBAR
const navbar = document.querySelector("nav");
window.addEventListener("scroll", () =>
    navbar.classList.toggle("sticky", window.scrollY > 0)
);

const menu = document.querySelector(".menu");
const toggleMenu = () => menu.classList.toggle("active");
document.querySelector(".menu-btn").addEventListener("click", toggleMenu);
document.querySelector(".close-btn").addEventListener("click", toggleMenu);
document.querySelectorAll(".menu a").forEach((link) =>
    link.addEventListener("click", toggleMenu)
);

// Form submit
async function predictAdoption(event) {
    event.preventDefault();

    const petData = {
        PetType: document.getElementById("PetType").value,
        Breed: document.getElementById("Breed").value,
        AgeMonths: parseInt(document.getElementById("AgeMonths").value),
        Color: "Unknown", // or add input field for color
        Size: document.getElementById("Size").value,
        WeightKg: parseFloat(document.getElementById("WeightKg").value),
        Vaccinated: parseInt(document.getElementById("Vaccinated").value),
        HealthCondition: parseInt(document.getElementById("HealthCondition").value),
        TimeInShelterDays: parseInt(document.getElementById("TimeInShelterDays").value),
        AdoptionFee: parseFloat(document.getElementById("AdoptionFee").value),
        PreviousOwner: parseInt(document.getElementById("PreviousOwner").value)
    };

    try {
        const response = await fetch("http://127.0.0.1:8000/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(petData)
        });

        const result = await response.json();

        const probability = result.adoption_probability;
        document.getElementById("result").innerText =
            `This pet has a ${probability}% chance of being adopted!`;
    } catch (error) {
        document.getElementById("result").innerText = "⚠️ Error connecting to API.";
        console.error(error);
    }
}
