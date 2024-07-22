
// Función para esconder el mensaje de alerta luego de 3 segundos
$(document).ready(function() {
    $(".alert").fadeTo(4000, 500).slideUp(500, function() { 
        $(".alert").slideUp(500);
      });
});

//Función para que la fecha máxima sean personas 18+
$(document).ready(function() {
  var fecha = new Date();

  var mes = fecha.getMonth() + 1;
  var dia = fecha.getDate();
  var anio = fecha.getFullYear() - 18;
  if(mes < 10)
      mes = '0' + mes;
  if(dia < 10)
      dia = '0' + dia;
  
  var fMax = anio + '-' + mes + '-' + dia;
  $('#fechaUsuario').attr('max', fMax);
});

$(".tarjeta").click(function() {
  var nombre = $(this).attr("id");
  var id = $("img", this).attr("id");
  window.location = "/ingreso-al-parqueo" + "/" + nombre + '&' + id;
});

$(document).ready(function() {
  if($("#semaforo").attr('src') == '/static/images/semaforoVerde.png'){
    $("#semaforo").fadeOut(7000, function(){
      $("#semaforo").attr("src","../static/images/semaforo.png");
      $("#semaforo").fadeIn()
    });
  }else if($("#semaforo").attr('src') == '/static/images/semaforoRojo.png'){
    $("#semaforo").fadeOut(7000, function(){
      $("#semaforo").attr("src","../static/images/semaforo.png");
      $("#semaforo").fadeIn()
    });
  }
});