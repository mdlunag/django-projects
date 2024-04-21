//Filters JS
const filtroForm = document.getElementById('filtro-form');
const filtroCheckboxes = document.querySelectorAll('input[name="labels"]');
const filtroTipos = document.querySelector('select[name="type"]');
const filtroMetodo = document.querySelector('select[name="method"]');

// Obtén una referencia al formulario y al select
const monthSelect = document.getElementById('month');

// Agrega un evento de cambio al select
monthSelect.addEventListener('change', function () {
    // Envía automáticamente el formulario cuando cambie la selección del mes
    filtroForm.submit();
});

filtroCheckboxes.forEach(checkbox => {
    checkbox.addEventListener('change', function () {
        filtroForm.submit(); // Envía automáticamente el formulario cuando cambia la selección
    });
});

filtroTipos.addEventListener('change', function () {
    filtroForm.submit(); // Envía automáticamente el formulario cuando cambia la selección
});

filtroMetodo.addEventListener('change', function () {
    filtroForm.submit(); // Envía automáticamente el formulario cuando cambia la selección
});

//JS for select2 field
$(document).ready(function() {
        // Inicializa el campo Select2
        $('.django-select2').select2();

        // Detecta cambios en el campo Select2
        $('.django-select2').on('change', function() {
            // Envía automáticamente el formulario cuando cambian las selecciones
            $('#filtro-form').submit();
        });
    });


async function getFinancialRecord(record_id, csrfToken) {
    try {
        const response = await fetch(`/${data.lang}/moneitas/api/get_financial_record/${record_id}/`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
        });
        
        if (!response.ok) {
            throw new Error('Failed to fetch financial record');
        }

        const registerData = await response.json();
        console.log(registerData)
        return registerData;
    } catch (error) {
        console.error('Error fetching financial record:', error);
        return null;
    }
}

$(document).ready(function() {
    // Almacena las dimensiones iniciales del logotipo
    var initialLogoWidth = $(".logo").width();
    var initialLogoHeight = $(".logo").height();

    $(window).scroll(function() {
        var scrollPosition = $(this).scrollTop();
        var navbarHeight = 100 - scrollPosition*0.8;
        navbarHeight = navbarHeight < 50 ? 50 : navbarHeight; // Limitar la altura mínima

        // Reduce gradualmente la altura de la barra de navegación
        $("#navbar").stop().animate({
            height: navbarHeight + "px"
        }, 10); // Duración de la animación en milisegundos (más largo para una transición más gradual)

        // Calcula las nuevas dimensiones del logotipo
        var newLogoWidth = initialLogoWidth * (navbarHeight / 100);
        var newLogoHeight = initialLogoHeight * (navbarHeight / 100);

        // Ajusta el tamaño del logotipo manteniendo sus proporciones originales
        $(".logo").stop().animate({
            width: newLogoWidth + "px",
            height: newLogoHeight + "px"
        }, 10); // Duración de la animación en milisegundos (más largo para una transición más gradual)

        // Calcula las nuevas dimensiones del logotipo
        var newNavbarTogglerSize = parseInt(initialNavbarTogglerSize) * (navbarHeight / 100);
        $(".navbar-toggler .navbar-toggler-icon").stop().animate({
            fontSize: newNavbarTogglerSize + "px"
        }, 10);

        // Ajusta el margen superior del contenido principal
        $(".main-content").css("margin-top", $("#navbar").height() + "px");
    });
});

