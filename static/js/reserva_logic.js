$(document).ready(function() {
    // Obtener las fechas inhabilitadas del atributo data-reserved-dates
    var reservedDates = $('[name="fecha"]').data('reserved-dates').split(',');

    // Configurar el campo de fecha con el datepicker
    $('[name="fecha"]').attr('readonly', true);
    $('[name="fecha"]').datepicker({
        dateFormat: 'yy-mm-dd',
        minDate: new Date(),
        beforeShowDay: function(date) {
            var stringDate = $.datepicker.formatDate('yy-mm-dd', date);
            return [reservedDates.indexOf(stringDate) === -1];
        },
        onSelect: function(dateText, inst) {
            // Acciones adicionales al seleccionar una fecha
        },
        // Configuración en español
        monthNames: ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'],
        monthNamesShort: ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'],
        dayNames: ['Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado'],
        dayNamesMin: ['Do', 'Lu', 'Ma', 'Mi', 'Ju', 'Vi', 'Sa'],
        firstDay: 1
    });

    // Mostrar el calendario al hacer clic en el ícono
    $('#cal-icon').click(function() {
        $('[name="fecha"]').datepicker('show');
    });
    
    
    
});

