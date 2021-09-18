$(document).ready(function () {

    $.ajax({
        type: "Get",
        url: "/api/v1/product",
        dataType: "json",
        success: function (resp) {
            for (let product of resp.results) {
                $('.content-row').append(`<div class="card col-3">
            <img class="card-img-top" src="{{ product.image }}" alt="Card image">
            <div class="card-body">
                <p class="card-text">{{ product.name }}</p>
                <div class="row" style="margin-left: 3px">
                    <i class="fa fa-fw fa-star" style="color: yellow; margin-top: 7px"></i>
                    <h4>{{ product.rate }}</h4>
                    <p style="margin-top: 4px">(۵۸)</p>
                </div>
                <div class="row" style="margin-left: 3px">
                    <p style="margin-top: 3px">تومان</p>
                    <h3>&nbsp26٫500٫000</h3>
                </div>
                <a href="#" class="stretched-link"></a>
            </div>
        </div>`)
            }
        }
    });
});