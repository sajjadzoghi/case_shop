$('#check-otp-btn').click(function (e) {
    e.preventDefault(); // avoid to execute the actual submit of the form.

    let register_form = $('#register-form')
    let data = register_form.serialize();

    $.ajax({
        type: "Post",
        url: `http://127.0.0.1:8000/api/v1/accounts/register/`,
        data: data,
        success: function (resp) {
            $('#register-form > .form-group').remove()
            $(register_form).append(`<div class="form-group">
                            <label for="verification">:کد تایید ارسالی را وارد کنید</label>
                            <input type="number" class="form-control" name="verification" id="verification" maxlength="6">
                        </div>`)
        }
    });
});