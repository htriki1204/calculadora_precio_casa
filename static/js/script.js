// Función para leer el archivo CSV
function leerCSV(url, callback) {
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200) {
            callback(xhr.responseText);
        }
    };
    xhr.open("GET", url, true);
    xhr.send();
}

// Función para generar opciones del menú desplegable
function generarOpciones(distritos) {
    var select = document.getElementById("district");
    distritos.forEach(function(distrito) {
        var option = document.createElement("option");
        option.value = distrito;
        option.textContent = distrito;
        select.appendChild(option);
    });
}

// Función para alternar el estado del botón entre "Sí" y "No" y cambiar el valor del campo oculto
function toggleButton(buttonId) {
    var button = document.getElementById(buttonId);
    var hiddenInput = document.getElementById(buttonId.split("Button")[0]);
    if (button.textContent === "Sí") {
        button.textContent = "No";
        hiddenInput.value = 0; // Establecer el valor como false (booleano)
    } else {
        button.textContent = "Sí";
        hiddenInput.value = 1; // Establecer el valor como true (booleano)
    }
}

// Llama a la función para leer el archivo CSV y generar opciones al cargar la página
leerCSV("../static/DistritosProduccion.csv", function(data) {
    var distritos = data.split("\n");
    generarOpciones(distritos);
});


$(document).ready(function() {
    // Manejar la solicitud del formulario
    $("#houseForm").submit(function(event) {
        // Prevenir el envío del formulario por defecto
        event.preventDefault();
        
        // Obtener los datos del formulario
        var formData = $(this).serialize();
        
        // Realizar una solicitud AJAX al servidor
        $.ajax({
            type: "POST",
            url: "/predict",
            data: formData,
            success: function(response) {
                // Verificar si hay un error en la respuesta
                if ("error" in response) {
                    // Mostrar el popup de error personalizado
                    showCustomPopup(response.error.join("\n"));
                } else {
                    // Procesar la respuesta normalmente
                }
            },
            error: function(xhr, status, error) {
                console.error("Error:", error);
            }
        });
    });
});

// Función para mostrar el popup personalizado
function showCustomPopup(message) {
    // Crear el elemento de popup
    var popup = $("<div class='popup'></div>");
    
    // Agregar el mensaje al popup
    popup.text(message);
    
    // Agregar el botón de cerrar
    var closeBtn = $("<span class='close-btn'>&times;</span>");
    closeBtn.click(function() {
        // Ocultar el popup al hacer clic en el botón de cerrar
        popup.remove();
    });
    popup.append(closeBtn);
    
    // Agregar el popup al cuerpo del documento
    $("body").append(popup);
}