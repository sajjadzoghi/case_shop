$('#register-form').submit(function (e) {
    e.preventDefault(); // avoid to execute the actual submit of the form.

    var form = $(this);
    console.log(form)

    var url = form.attr('action');
    var form_data = new FormData(this);
    console.log(form_data);

    $.ajax({
        type: "post",
        url: url,
        data: form_data,
        success: function (resp) {
            console.log(resp)
            if (typeof resp.detail !== 'undefined') {
                $('#register-form > .form-group').hide('fast');
                $('#send-info-btn').attr('id', 'verify-otp-btn');
                $('#verify-otp-btn').html('ارسال');
                $('#register-form').append(`<div class="form-group" id="otp-group">
                            <label for="otp">:کد تایید ارسال‌شده به گوشی را وارد کنید</label>
                            <input type="number" class="form-control" name="otp" id="otp" maxlength="6">
                        </div>`)
                $('#otp-group').show('fast');
            } else {
                $('#mobile-group').append(`<p>${resp.detail}</p>`)
            }

            $('#register-form').trigger('reset');
        },
        cache: false,
        contentType: false,
        processData: false

    });

});

$('#verify-otp-btn').click(function (e) {
    e.preventDefault(); // avoid to execute the actual submit of the form.

    let register_form = $('#register-form')
    let data = register_form.serialize();

    $.ajax({
        type: "Post",
        url: `http://127.0.0.1:8000/api/v1/accounts/verify/`,
        data: data,
        success: function (resp) {
            if (typeof resp.detail !== 'undefined') {
                $('#register-form > .form-group').hide('fast');
                $('#register-form').append(`<p>${resp.approved}</p>`)
            } else {
                $('#otp-group').append(`<p>${resp.detail}</p>`)
            }
        },
        cache: false,
        contentType: false,
        processData: false
    })
});