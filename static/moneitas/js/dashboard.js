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


