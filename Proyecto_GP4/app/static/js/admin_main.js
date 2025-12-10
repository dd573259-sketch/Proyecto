const btnAccesibilidad = document.querySelector(".btn-accesibilidad");
const menuAccesibilidad = document.getElementById("menuAccesibilidad");
let fontSize = 100;

// Mostrar/Ocultar
btnAccesibilidad.addEventListener("click", () => {
    menuAccesibilidad.style.display =
        menuAccesibilidad.style.display === "flex" ? "none" : "flex";
});

// oscuro
document.getElementById("modoOscuro").addEventListener("click", () => {
    document.body.classList.toggle("dark-mode");
});

// Aumentar
document.getElementById("aumentar").addEventListener("click", () => {
    fontSize += 10;
    document.body.style.fontSize = fontSize + "%";
});

// Disminuir
document.getElementById("disminuir").addEventListener("click", () => {
    if (fontSize > 50) {
        fontSize -= 10;
        document.body.style.fontSize = fontSize + "%";
    }
});

document.getElementById("restablecer").addEventListener("click", () => {
    fontSize = 100;
    document.body.style.fontSize = "100%";
});// Restablecer tamaño

document.getElementById("contraste").addEventListener("click", () => {
    document.body.classList.toggle("high-contrast");
});// Alto contraste