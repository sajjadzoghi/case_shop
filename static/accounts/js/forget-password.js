let forget_btn = $('#forget-btn');

function forget_password() {
    $('.reset-choices').remove()
    $(forget_btn).after(`<button class="reset-choices" onclick="reset_by_mobile()">بازیابی از طریق شماره موبایل</button>`);
    $(forget_btn).after(`<button class="reset-choices" onclick="reset_by_email()">بازیابی از طریق ایمیل</button>`);
}

function reset_by_mobile() {
    $('#reset-password-mobile-modal').modal('show');
}

function reset_by_email() {
    $('#reset-password-email-modal').modal('show');
}

$('#reset-password-mobile-form').submit(function (e) {
    e.preventDefault(); // avoid to execute the actual submit of the form.

    var form = $(this);
    var url = form.attr('action');
    var form_data = {
        'mobile': $('#reset-password-mobile').val(),
    };

    $.ajax({
        type: "post",
        url: url,
        data: form_data,
        success: function (resp) {
            $('#reset-password-mobile-modal').modal('hide');
            $('#reset-password-otp-form #otp-again').remove();
            $('#reset-password-otp-group label').html('لطفاً کد تأیید ۶رقمی ارسال شده به گوشی خود را وارد کنید');
            $('#reset-user').attr('value', resp.mobile);
            $('#auth-type').attr('value', 'mobile');
            $('#reset-password-otp-modal').modal('show');
        },
        error: function (data) {
            $('#reset-password-mobile-form p').remove();
            let errors = JSON.parse(data.responseText);
            for (let error_item in errors) {
                $(form).prepend(`<p class="text-danger">${errors[error_item][0]}*</p>`);
            }
        }
    });
});

$('#reset-password-email-form').submit(function (e) {
    e.preventDefault(); // avoid to execute the actual submit of the form.

    var form = $(this);
    var url = form.attr('action');
    var form_data = {
        'email': $('#reset-password-email').val(),
    };

    $.ajax({
        type: "post",
        url: url,
        data: form_data,
        success: function (resp) {
            $('#reset-password-email-modal').modal('hide');
            $('#reset-password-otp-form #otp-again').remove();
            $('#reset-password-otp-group label').html('کد تأییدی ۶رقمی به ایمیل شما ارسال شد. لطفاً آن را در فیلد زیر وارد کنید')
            $('#reset-user').attr('value', resp.email);
            $('#auth-type').attr('value', 'email');
            $('#reset-password-otp-modal').modal('show');
        },
        error: function (data) {
            $('#reset-password-email-form p').remove();
            let errors = JSON.parse(data.responseText);
            for (let error_item in errors) {
                $(form).prepend(`<p class="text-danger">${errors[error_item][0]}*</p>`);
            }
        }
    });
});

$('#reset-password-otp-form').submit(function (e) {
    e.preventDefault(); // avoid to execute the actual submit of the form.

    var form = $(this);
    var url = form.attr('action');
    var auth_type = $('#auth-type').val();
    var form_data = {
        'info': $('#reset-user').val(),
        'otp': $('#reset-password-otp').val(),
    };

    $.ajax({
        type: "post",
        url: url,
        data: form_data,
        success: function (resp) {
            $('#reset-password-otp-modal').modal('hide');
            $('#reset-user-final').attr('value', resp.mobile);
            $('#new-reset-password-group label').html(`:${resp.first_name} عزیز، رمز عبور جدید خود را وارد کنید`)
            $('#reset-password-mobile-form .form-group').show();
            $('#reset-password-mobile-form .btn-group').show();
            $('#reset-password-mobile-form h5').remove();
            $('#reset-password-mobile-form #close').remove();
            $('#new-reset-password-modal').modal('show');
            $('#reset-password-email-form').trigger('reset');
            $('#reset-password-mobile-form').trigger('reset');
        },
        error: function (data) {
            $('#reset-password-otp-form p').remove();
            let errors = JSON.parse(data.responseText);
            for (let error_item in errors) {
                $(form).prepend(`<p class="text-danger">${errors[error_item][0]}*</p>`);
            }
            $(form).append(`<button id="otp-again" onclick="$('#reset-password-${auth_type}-form').submit()" class="btn-primary">ارسال مجدد</button>`);
        }
    });
});

$('#new-reset-password-form').submit(function (e) {
    e.preventDefault(); // avoid to execute the actual submit of the form.

    var form = $(this);
    var url = form.attr('action');
    var form_data = {
        'mobile': $('#reset-user-final').val(),
        'new_password': $('#new-reset-password').val(),
    };

    $.ajax({
        type: "post",
        url: url,
        data: form_data,
        success: function (resp) {
            $('#new-reset-password-form .form-group').hide('slow');
            $('#new-reset-password-form .btn-group').hide('slow');
            $(form).trigger('reset');
            $('#new-reset-password-form p').remove();
            $(form).prepend(`<h5 class="text-success">«${resp.first_name} عزیز، تغییر رمز عبور شما با موفقیت انجام شد»</h5>`);
            $(form).append(`<button type="button" id="close" class="btn btn-danger" data-dismiss="modal">بستن</button>`);
        },
        error: function (data) {
            $('#new-reset-password-form p').remove();
            let errors = JSON.parse(data.responseText);
            for (let error_item in errors) {
                $(form).prepend(`<p class="text-danger">${errors[error_item][0]}*</p>`);
            }
        }
    });
});