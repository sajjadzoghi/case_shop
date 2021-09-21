/*
jQuery & AJAX for showing all products with pagination
*/

$.ajax({
    type: "Get",
    url: "http://127.0.0.1:8000/api/v1/products/",
    dataType: "json",
    success: function (resp) {
        for (let product of resp.results) {
            $('.content-row').append(`<div class="card col-3">
                <img class="card-img-top" src="${product.image}" alt="Card image">
                <div class="card-body">
                    <p class="card-text">${product.name}</p>
                    <div class="row" style="margin-left: 3px">
                        <i class="fa fa-fw fa-star" style="color: yellow;font-size: 15px;margin-top: 7px"></i>
                        <h4>${product.rate_average}</h4>
                        <p style="margin-top: 4px">(${product.voters_number}دیدگاه)</p>
                    </div>
                    <div class="row" style="margin-left: 3px">
                        <p style="margin-top: 3px">تومان</p>
                        <h3>&nbsp${product.final_price}</h3>
                    </div>
                    <a href="#" class="stretched-link"></a>
                </div>
            </div>`)
        }

        $('.pagination').append(`<a id="previous" onclick="prev_next(${resp.previous})">&laquo;</a>`)
        for (let i = 1; i <= resp.num_pages; i++) {
            $('.pagination').append(`
              <a onclick="products(${i})">${i}</a>`)
        }
        $('.pagination').append(`<a id="next" onclick="prev_next(${resp.next})">&raquo;</a>`);

        if (resp.next == null) {
            $('#next').disabled;
        } else if (resp.previous == null) {
            $('#previous').disabled;
        }
    }
});

function products(i) {
    $.ajax({
        type: "Get",
        url: `http://127.0.0.1:8000/api/v1/products/?page=${i}`,
        dataType: "json",
        success: function (resp) {
            $('.content-row').empty();
            for (let product of resp.results) {
                $('.content-row').append(`<div class="card col-3">
                <img class="card-img-top" src="${product.image}" alt="Card image">
                <div class="card-body">
                    <p class="card-text">${product.name}</p>
                    <div class="row" style="margin-left: 3px">
                        <i class="fa fa-fw fa-star" style="color: yellow;font-size: 15px;margin-top: 7px"></i>
                        <h4>${product.rate_average}</h4>
                        <p style="margin-top: 4px">(${product.voters_number}دیدگاه)</p>
                    </div>
                    <div class="row" style="margin-left: 3px">
                        <p style="margin-top: 3px">تومان</p>
                        <h3>&nbsp${product.final_price}</h3>
                    </div>
                    <a href="#" class="stretched-link"></a>
               </div>
            </div>`)
            }

            $('.pagination').empty();
            $('.pagination').append(`<a id="previous" onclick="prev_next(${resp.previous})">&laquo;</a>`)
            for (let i = 1; i <= resp.num_pages; i++) {
                $('.pagination').append(`
              <a onclick="products(${i})">${i}</a>`)
            }
            $('.pagination').append(`<a id="next" onclick="prev_next(${resp.next})">&raquo;</a>`);

            if (resp.next == null) {
                $('#next').disabled;
            } else if (resp.previous == null) {
                $('#previous').disabled;
            }
        }
    });
}

function prev_next(url) {
    console.log(url)
    if (url != null) {
        $.ajax({
            type: "Get",
            url: `${url}`,
            dataType: "json",
            success: function (resp) {
                $('.content-row').empty();
                for (let product of resp.results) {
                    $('.content-row').append(`<div class="card col-3">
                    <img class="card-img-top" src="${product.image}" alt="Card image">
                    <div class="card-body">
                        <p class="card-text">${product.name}</p>
                        <div class="row" style="margin-left: 3px">
                            <i class="fa fa-fw fa-star" style="color: yellow;font-size: 15px;margin-top: 7px"></i>
                            <h4>${product.rate_average}</h4>
                            <p style="margin-top: 4px">(${product.voters_number}دیدگاه)</p>
                        </div>
                        <div class="row" style="margin-left: 3px">
                            <p style="margin-top: 3px">تومان</p>
                            <h3>&nbsp${product.final_price}</h3>
                        </div>
                        <a href="#" class="stretched-link"></a>
                    </div>
                </div>`)
                }

                $('.pagination').empty();
                $('.pagination').append(`<a id="previous" onclick="prev_next(${resp.previous})">&laquo;</a>`)
                for (let i = 1; i <= resp.num_pages; i++) {
                    $('.pagination').append(`
              <a onclick="products(${i})">${i}</a>`)
                }
                $('.pagination').append(`<a id="next" onclick="prev_next(${resp.next})">&raquo;</a>`);

                if (resp.next == null) {
                    $('#next').disabled;
                } else if (resp.previous == null) {
                    $('#previous').disabled;
                }
            }
        });
    }
}