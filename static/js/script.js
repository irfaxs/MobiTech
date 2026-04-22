function goToForm(brand) {
    document.getElementById("formSection").style.display = "block";
    document.getElementById("brandInput").value = brand;
    document.getElementById("selectedBrand").innerText = brand;

    // smooth scroll
    document.getElementById("formSection").scrollIntoView({
        behavior: 'smooth'
    });
}

function showPrice() {
    let condition = document.getElementById("condition").value;
    let price = 20000;

    if (condition === "Good") price = 15000;
    if (condition === "Poor") price = 8000;

    document.getElementById("price").innerText = price;
    document.getElementById("priceBox").style.display = "block";

    document.getElementById("priceBox").scrollIntoView({
        behavior: 'smooth'
    });
}






