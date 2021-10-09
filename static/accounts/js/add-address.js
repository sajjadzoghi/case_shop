// scripts for handling "province and city" selection

function Func(cities) {
    var city = document.getElementById("city");
    city.options.length = 0;
    if (cities != "") {
        var arr = cities.split(",");
        for (i = 0; i < arr.length; i++) {
            if (arr[i] != "") {
                city.options[city.options.length] = new Option(arr[i], arr[i]);
            }
        }
    }
}