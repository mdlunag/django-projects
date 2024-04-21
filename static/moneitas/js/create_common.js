let labelPlaceholder = $('#id_label_existente')[0][0];
let labelPlaceholderText =  $('#id_label_existente')[0][0].text;

// Función para cargar las labels disponibles según el type seleccionado
function cargarEtiquetasDisponibles(typeSeleccionado, labelPlaceholder) {
    var labelsSelect = $('#id_label_existente');
    labelsSelect.empty();
    labelsSelect.append(labelPlaceholder);
    if (typeSeleccionado){
        labelPlaceholder.text = labelPlaceholderText;
        $.ajax({
            url: '/moneitas/get_labels/',  // Cambia la URL a la que corresponda en tu proyecto
            data: {'type': typeSeleccionado},
            dataType: 'json',
            success: function(data) {
                // Actualiza las opciones del campo de labels
                $.each(data.labels, function(index, label) {
                    labelsSelect.append($('<option></option>').attr('value', label.id).text(label.name));
                });
            }
    })};
}

$( window ).on( "load", function(){
    console.log('onload');
    if($('#type-income').prop('checked') || $('#type-expense').prop('checked')){
        var inputType = $('#type-income').prop('checked')?'income':'expense';
        var labelSelected = $('#id_label_existente').find(':selected');
        console.log(inputType);
        cargarEtiquetasDisponibles(inputType, labelSelected);
      }
    else {
        let labelPlaceholderini = labelPlaceholder;
        labelPlaceholderini.text = 'Por favor selecciona el tipo';
        cargarEtiquetasDisponibles('', labelPlaceholderini);
    };
}),
$(document).ready(function() {

     // Detecta clic en botón de Ingreso
    $('#type-income').click(function() {
        $("p[name='paid']").show();
        cargarEtiquetasDisponibles('income', labelPlaceholder);
    });

    // Detecta clic en botón de Gasto
    $('#type-expense').click(function() {
        $("p[name='paid']").hide();
        cargarEtiquetasDisponibles('expense', labelPlaceholder);
    });

});

const data = document.currentScript.dataset;

//Mark register as paid
function EditRegister(field_name, value, model_name, record_id) {
    var csrfToken = document.cookie.match(/csrftoken=([\w-]+)/)[1];
    var dictData = {};
    dictData[field_name] = value;
    fetch('/' + data.lang + `/moneitas/api/edit_${model_name}/${record_id}/`,{
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