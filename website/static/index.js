
// Función para esconder el mensaje de alerta luego de 3 segundos
$(document).ready(function() {
    $(".alert").fadeTo(3000, 500).slideUp(500, function() { 
        $(".alert").slideUp(500);
      });
});