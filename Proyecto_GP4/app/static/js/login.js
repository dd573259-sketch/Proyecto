document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("loginForm");
  const usuario = document.getElementById("usuario");
  const contrasena = document.getElementById("contrasena");
  const errorUsuario = document.getElementById("errorUsuario");
  const errorContrasena = document.getElementById("errorContrasena");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    // limpiar mensajes previos
    errorUsuario.textContent = "";
    errorContrasena.textContent = "";

    const formData = new FormData(form);

    try {
      const response = await fetch("validar.php", {
        method: "POST",
        body: formData
      });

      const result = await response.text();

      if (result === "usuario") {
        errorUsuario.textContent = "Usuario incorrecto";
        errorUsuario.style.color = "red";
      } else if (result === "contrasena") {
        errorContrasena.textContent = "Contraseña incorrecta";
        errorContrasena.style.color = "red";
      } else if (result === "error_general") {
        alert("Error en la conexión con la base de datos");
      } else {
        // Si devuelve una ruta, redirigimos
        window.location.href = result;
      }
    } catch (error) {
      alert("Error en el sistema: " + error.message);
    }
  });
});