// Prefill search engine from url parameters
let params = new URLSearchParams(document.location.search);
let beer_type = params.get("beer_type") || "";

document.querySelector(".beer_type").value = beer_type;

function searchBeers() {
    // Take the beer type
    beercocktailTypeSelect = document.querySelector(".beer_type");
    beerType = beercocktailTypeSelect.value || "";

    // Send the request and refresh the page
    var url = new URL(window.location);
    if (beerType != "") { url.searchParams.set("beer_type", beerType); }
    else { url.searchParams.delete("beer_type"); }

    window.location = url;
}
