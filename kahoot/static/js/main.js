document.addEventListener('DOMContentLoaded', function () {
    const addOptionBtn = document.getElementById('add-option-btn');
    const optionFormsDiv = document.getElementById('option-forms');
    const totalFormsInput = document.getElementById('id_options-TOTAL_FORMS');
    let formCount = parseInt(totalFormsInput.value);

    addOptionBtn.addEventListener('click', function () {
        if (formCount < {{ option_formset.max_num }}) {  // Respect the max_num limit
            const newFormHtml = `
                <div class="option-form">
                    ${optionFormsDiv.firstElementChild.innerHTML.replace(/__prefix__/g, formCount)}
                </div>
            `;
            optionFormsDiv.insertAdjacentHTML('beforeend', newFormHtml);
            formCount++;
            totalFormsInput.value = formCount;
        } else {
            alert('You can add a maximum of {{ option_formset.max_num }} options.');
        }
    });
});
