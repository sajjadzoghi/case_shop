$('#register-form').submit(function (e) {
    e.preventDefault(); // avoid to execute the actual submit of the form.

    var form = $(this);
    var url = form.attr('action');
    var form_data = {
        'mobile': $('#reg-mobile').val(),
        'first_name': $('#first_name').val(),
        'last_name': $('#last_name').val(),
        'email': $('#email').val(),
        'password': $('#reg-password').val(),
    };

    $.ajax({
        type: "post",
        url: url,
        data: form_data,
        success: function (resp) {
            // $('#send-info-btn').attr('data-dismiss', 'modal');
            $('#register-modal').modal('hide');
            $('#otp-form #otp-group').show();
            $('#otp-btn-group').show();
            $('#otp-form h5').remove();
            $('#otp-form #close').remove();
            $('#otp-form #otp-again').remove();
            $('#otp-modal').modal('show');
            $('form p').remove();
        },
        error: function (data) {
            $('form p').remove();
            let errors = JSON.parse(data.responseText);
            for (let error_item in errors) {
                $(form).prepend(`<p class="text-danger">${errors[error_item][0]}*</p>`);
            }
        }
    });

});

$('#otp-form').submit(function (e) {
    e.preventDefault(); // avoid to execute the actual submit of the form.

    let form = $(this)
    let form_data = {
        'mobile': $('#reg-mobile').val(),
        'first_name': $('#first_name').val(),
        'last_name': $('#last_name').val(),
        'email': $('#email').val(),
        'password': $('#reg-password').val(),
        'otp': $('#otp').val(),
    };

    $.ajax({
        type: "Post",
        url: `http://127.0.0.1:8000/api/v1/accounts/verify/`,
        data: form_data,
        success: function (resp) {
            $('form #otp-group').hide('slow');
            $('form #otp-btn-group').hide('slow');
            $(form).trigger('reset');
            $('form p').remove();
            $(form).prepend(`<h5 class="text-success">«${$('#first_name').val()} عزیز، ثبت‌نام شما با موفقیت انجام شد»</h5>`);
            $(form).append(`<button type="button" id="close" class="btn btn-danger" data-dismiss="modal">بستن</button>`);
            $('#register-form').trigger('reset');
        },
        error: function (data) {
            $('form p').remove();
            let errors = JSON.parse(data.responseText);
            for (let error_item in errors) {
                $(form).prepend(`<p class="text-danger">${errors[error_item][0]}*</p>`);
            }
            $(form).append(`<button id="otp-again" onclick="$('#register-form').submit()" class="text-danger">ارسال مجدد</button>`);
        }
    });
});