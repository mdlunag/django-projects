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

// Financial records selection for deletion
$(document).ready(function() {
            
    $('.clickable').click(function () {
        console.log(this);
        var _delete = this.closest('tr').querySelector("input[id='_delete']")
        //Check to see if background color is set or if it's set to white.
        if(this.closest('tr').style.background != "lightblue") {
            $(this).closest('tr').css('background', 'lightblue');
            $(this).closest('tr').css('color', 'blue');
            console.log(_delete);
            _delete.checked = true;
        }
        else {
            _delete.checked = false;
            if(this.closest('tr').className == 'income'){
                $(this).closest('tr').css('background', '#a5d6a7');
                $(this).closest('tr').css('color', '#006400');
            }
            else {
                $(this).closest('tr').css('background', '#ffcdd2');
                $(this).closest('tr').css('color', '#b71c1c');
            }
            if (screen.width <768){
            $("#delete-btn").toggle($(this).find(".delete-checkbox:checked").length = 0);
            }
           
        }
        if (screen.width <768){
            var checkedToDelete = $(".delete-checkbox:checked").length;
            console.log(checkedToDelete);
            if(checkedToDelete > 0){
                $("#delete-btn").show();
                $(".btn-crear-phone").hide();
            }else if(checkedToDelete == 0){
                $("#delete-btn").hide();
                $(".btn-crear-phone").show();
            }}
    });
    $('.payment-method').click(function() {
        $('i', this).toggleClass("fa-regular fa-credit-card fa-solid fa-money-bill-1");
    });

    $('.btn-delete-phone').click(function() {
        $('#financial-records').submit();
    });
});

const data = document.currentScript.dataset;

//Mark register as paid
function EditRegister(field_name, value,record_id) {
    var csrfToken = document.cookie.match(/csrftoken=([\w-]+)/)[1];
    var dictData = {};
    dictData[field_name] = value;
    fetch('/' + data.lang + `/moneitas/api/edit_financial_record/${record_id}/`,{
        method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify(dictData)
        })
   
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();  // Si esperas una respuesta en JSON
        })
        .then(data => {
            console.log('Tarea editada:', data);
    
        })
        .catch(error => console.error('Error:', error));
    if (field_name == "income_paid"){
        var paidElement = document.getElementById("paidIncomes");
        var currentPaidIncomes =  parseInt(paidElement.textContent);
        getFinancialRecord(record_id, csrfToken).then(
            result => {
            registerAmount = parseInt(result.amount);
            if (value){
                paidElement.textContent = currentPaidIncomes+ registerAmount;
            }else{
                paidElement.textContent = currentPaidIncomes- registerAmount;
            }
            console.log(registerAmount, paidElement.textContent)

        }
        ).catch(error => {
            // Manejar cualquier error aquí
            console.error('Error fetching financial record:', error);
        });
    }
};


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