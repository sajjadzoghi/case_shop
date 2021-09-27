let forget_btn = $('#forget-btn');
let content = $('.content-row');
let login_form = $('#login-form');

function forget_password() {
    $(forget_btn).after(`<button onclick="reset_by_mobile()">تغییررمز از طریق شماره موبایل</button>`);
    $(forget_btn).after(`<button onclick="reset_by_email()">تغییررمز از طریق ایمیل</button>`);
}

function reset_by_mobile() {
    $(forget_btn).hide('slow');
    $(login_form).hide('slow');
    $('.content-row .card').append(`
            <form method="post" id="reset-password-mobile">
                <div class="form-group" id="reset-mobile-group">
                    <label for="reset-mobile">:شماره موبایل خود را وارد کنید</label>
                    <input type="text" class="form-control" name="reset-mobile" id="reset-mobile">
                </div>
                <div class="btn-group">
                    <button type="button" class="btn btn-danger"><a href="http://127.0.0.1:8000/accounts/login/">انصراف</a></button>
                    <button type="submit" class="btn btn-submit mr-3" id="reset-btn-forget">ارسال
                    </button>
                </div>
            </form>`);
}

$('#reset-password-mobile').submit(function (e) {
    e.preventDefault(); // avoid to execute the actual submit of the form.

    var form = $(this);
    var url = "http://127.0.0.1:8000/api/v1/accounts/mobile-password-reset/";
    var form_data = form.serialize();

    $.ajax({
        type: "post",
        url: url,
        data: form_data,
        success: function (resp) {
            $(form).hide('slow');
            $('.content-row .card').append(`
            <p>${resp.first_name} عزیز، رمز عبور شما </p>`)
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

function reset_by_email() {
    $(forget_btn).hide('slow');
    $(login_form).hide('slow');
    $('.content-row .card').append(`
            <form method="post" id="reset-form-email">
                <div class="form-group" id="reset-email-group">
                    <label for="reset-email">:ایمیل خود را وارد کنید</label>
                    <input type="email" class="form-control" name="reset-email" id="reset-email">
                </div>
                <div class="btn-group">
                    <button type="button" class="btn btn-danger"><a href="http://127.0.0.1:8000/accounts/login/">انصراف</a></button>
                    <button type="submit" class="btn btn-submit mr-3" id="reset-btn-forget">ارسال
                    </button>
                </div>
            </form>`);
}

$('#reset-form-email').submit(function (e) {
    e.preventDefault(); // avoid to execute the actual submit of the form.

    var form = $(this);
    var url = "http://127.0.0.1:8000/api/v1/accounts/password_reset/";
    var form_data = form.serialize();

    $.ajax({
        type: "post",
        url: url,
        data: form_data,
        success: function () {
            $(form).hide('slow');
            $('.content-row .card').append(`
            <form method="POST" id="reset-password-by-email">
                <div class="form-group" id="new-password">
                    <label for="new-password">:رمز عبور جدید</label>
                    <input type="text" class="form-control" name="new-password" id="new-password">
                </div>
                <div class="btn-group">
                    <button type="button" class="btn btn-danger"><a href="http://127.0.0.1:8000/accounts/login/">انصراف</a></button>
                    <button type="submit" class="btn btn-submit mr-3" id="reset-btn-forget">ارسال
                    </button>
                </div>
            </form>`)
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

$('#reset-password-by-email').submit(function (e) {
    e.preventDefault(); // avoid to execute the actual submit of the form.

    var form = $(this);
    var url = "http://127.0.0.1:8000/api/v1/accounts/password_reset/confirm/";
    var form_data = form.serialize();

    $.ajax({
        type: "post",
        url: url,
        data: form_data,
        success: function () {
            $(form).hide('slow');
            $('.content-row .card').append(`<p>تغییر رمز عبور با موفقیت انجام شد. اکنون می‌توانید از <a class="text-danger" href="http://127.0.0.1:8000/accounts/login/">اینجا</a> وارد شوید.</p>`)
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