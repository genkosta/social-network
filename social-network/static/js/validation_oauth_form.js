$(document).ready(function() {
    $(document).on('submit', 'form', function (event) {
        var $form = $(this);
        if ($form.find('select[name=client_type] option:selected').val() != 'confidential') {
            event.preventDefault();
            alert('Client type - Допустимое значение: Confidential');
        } else if ($form.find('select[name=authorization_grant_type] option:selected').val() != 'authorization-code') {
            event.preventDefault();
            alert('Authorization grant type - Допустимое значение: Authorization code');
        }
    });
});
