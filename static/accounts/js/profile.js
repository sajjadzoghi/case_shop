$('#change-password-form').submit(function (e) {
    e.preventDefault(); // avoid to execute the actual submit of the form.

    var form = $(this);
    var url = form.attr('action');
    var $crf_token = $('#change-password-form [name="csrfmiddlewaretoken"]').attr('value');

    var form_data = {
        'old_password': $('#old-password').val(),
        'new_password': $('#new-password').val(),
        'new_password2': $('#new-password2').val(),
    };

    $.ajax({
        type: "put",
        url: url,
        data: form_data,
        headers: {"X-CSRFToken": $crf_token},
        success: function () {
            $('#change-password-form p').remove();
            alert('« رمز عبور شما با موفقیت تغییر کرد. »');
            form.trigger('reset');
            window.location.href = "/accounts/login/"
        },
        error: function (data) {
            $('#change-password-form p').remove();
            let errors = JSON.parse(data.responseText);
            for (let error_item in errors) {
                $(form).prepend(`<p class="text-danger">* ${errors[error_item][0]}</p>`);
            }
        }
    });

});


$('#add-address-form').submit(function (e) {
    e.preventDefault(); // avoid to execute the actual submit of the form.

    var form = $(this);
    var url = form.attr('action');
    var $crf_token = $('#add-address-form [name="csrfmiddlewaretoken"]').attr('value');

    var form_data = {
        'province': $('#add-province').val(),
        'city': $('#add-city').val(),
        'exact_address': $('#add-exact_address').val(),
        'apartment_number': $('#add-No').val(),
        'unit': $('#add-unit').val(),
        'zip_code': $('#add-zip_code').val(),
    };

    $.ajax({
        type: "post",
        url: url,
        data: form_data,
        headers: {"X-CSRFToken": $crf_token},
        success: function () {
            $('#add-address-form p').remove();
            form.trigger('reset');
            $('#add-address-modal').modal('hide');
            alert('« آدرس با موفقیت اضافه شد. »');
            window.location.href = "/accounts/profile/"
        },
        error: function (data) {
            $('#add-address-form p').remove();
            let errors = JSON.parse(data.responseText);
            for (let error_item in errors) {
                $(form).prepend(`<p class="text-danger">* ${errors[error_item][0]}</p>`);
            }
        }
    });

});


function edit_address_submit(address_id) {
    $(`#edit-address-form${address_id}`).submit(function (e) {
        e.preventDefault(); // avoid to execute the actual submit of the form.

        var form = $(this);
        var url = form.attr('action');
        var $crf_token = $(`#edit-address-form${address_id} [name="csrfmiddlewaretoken"]`).attr('value');

        var form_data = {
            'province': $(`#province${address_id}`).val(),
            'city': $(`#city${address_id}`).val(),
            'exact_address': $(`#exact_address${address_id}`).val(),
            'apartment_number': $(`#No${address_id}`).val(),
            'unit': $(`#unit${address_id}`).val(),
            'zip_code': $(`#zip_code${address_id}`).val(),
        };

        $.ajax({
            type: "put",
            url: url,
            data: form_data,
            headers: {"X-CSRFToken": $crf_token},
            success: function () {
                $(`#edit-address-form${address_id} p`).remove();
                form.trigger('reset');
                $(`#edit-address-modal${address_id}`).modal('hide');
                alert('« آدرس با موفقیت ویرایش شد. »');
                window.location.href = "/accounts/profile/"
            },
            error: function (data) {
                $(`#edit-address-form${address_id} p`).remove();
                let errors = JSON.parse(data.responseText);
                for (let error_item in errors) {
                    $(form).prepend(`<p class="text-danger">* ${errors[error_item][0]}</p>`);
                }
            }
        });

    });
}

function delete_address_submit(address_id) {
    $(`#delete-address-form${address_id}`).submit(function (e) {
        e.preventDefault(); // avoid to execute the actual submit of the form.

        var form = $(this);
        var url = form.attr('action');
        var $crf_token = $(`#delete-address-form${address_id} [name="csrfmiddlewaretoken"]`).attr('value');

        $.ajax({
            type: "delete",
            url: url,
            headers: {"X-CSRFToken": $crf_token},
            success: function () {
                $(`#delete-address-form${address_id} p`).remove();
                $(`#delete-address-modal${address_id}`).modal('hide');
                alert('« آدرس با موفقیت حذف شد. »');
                window.location.href = "/accounts/profile/"
            },
            error: function (data) {
                $(`#delete-address-form${address_id} p`).remove();
                let errors = JSON.parse(data.responseText);
                for (let error_item in errors) {
                    $(form).prepend(`<p class="text-danger">* ${errors[error_item][0]}</p>`);
                }
            }
        });
    });
}


$('#change-mobile-form').submit(function (e) {
    e.preventDefault(); // avoid to execute the actual submit of the form.

    var form = $(this);
    var url = form.attr('action');
    var $crf_token = $(`#change-mobile-form [name="csrfmiddlewaretoken"]`).attr('value');

    var form_data = {
        'mobile': $('#new-mobile').val(),
    };

    $.ajax({
        type: "put",
        url: url,
        data: form_data,
        headers: {"X-CSRFToken": $crf_token},
        success: function () {
            $('#change-mobile-modal').modal('hide');
            $('#change-mobile-otp-form #change-mobile-otp-group').show();
            $('#change-mobile-otp-btn-group').show();
            $('#change-mobile-otp-form h5').remove();
            $('#change-mobile-otp-form #close').remove();
            $('#change-mobile-otp-form #change-mobile-otp-again').remove();
            $('#change-mobile-otp-form p').remove();
            $('#change-mobile-otp-modal').modal('show');
            $('#change-mobile-form p').remove();
        },
        error: function (data) {
            $('#change-mobile-form p').remove();
            let errors = JSON.parse(data.responseText);
            for (let error_item in errors) {
                $(form).prepend(`<p class="text-danger">${errors[error_item][0]}*</p>`);
            }
        }
    });

});

$('#change-mobile-otp-form').submit(function (e) {
    e.preventDefault(); // avoid to execute the actual submit of the form.

    let form = $(this);
    let url = form.attr('action');
    var $crf_token = $(`#change-mobile-otp-form [name="csrfmiddlewaretoken"]`).attr('value');

    let form_data = {
        'mobile': $('#new-mobile').val(),
        'otp': $('#change-mobile-otp').val(),
    };

    $.ajax({
        type: "put",
        url: url,
        data: form_data,
        headers: {"X-CSRFToken": $crf_token},
        success: function () {
            $('#change-mobile-otp-form #change-mobile-otp-group').hide('slow');
            $('#change-mobile-otp-form #change-mobile-otp-btn-group').hide('slow');
            $(form).trigger('reset');
            $('#change-mobile-otp-form p').remove();
            $('#id_mobile').val($('#new-mobile').val());
            $(form).prepend(`<h5 class="text-success">« شماره موبایل جدید شما با موفقیت ثبت شد. »</h5>`);
            $(form).append(`<button type="button" id="close" class="btn btn-danger mr-0" data-dismiss="modal">بستن</button>`);
            $('#change-mobile-form').trigger('reset');
        },
        error: function (data) {
            console.log(data.responseText)
            $('#change-mobile-otp-form #change-mobile-otp-again').remove();
            $('#change-mobile-otp-form p').remove();
            let errors = JSON.parse(data.responseText);
            for (let error_item in errors) {
                $(form).prepend(`<p class="text-danger">${errors[error_item][0]}*</p>`);
            }
            $(form).append(`<div id="change-mobile-otp-again" onclick="$('#change-mobile-form').submit()" class="btn btn-secondary mr-0 mt-2">ارسال مجدد</div>`);
        }
    });
});