document.getElementById("calculate").addEventListener("click", function () {
    // const unsubsidizedValue = document.getElementById("unsubsidized").value;
    // console.log("Unubsidized input value:", "4", unsubsidizedValue);
    
    const unsubsidized = parseFloat(document.getElementById("unsubsidized").value);
    const subsidized = parseFloat(document.getElementById("subsidized").value);
    const interest = parseFloat(document.getElementById("interest").value);
    const monthlyPayment = parseFloat(document.getElementById("monthlyPayment").value.trim());

    const success = "success";
    // Create a string with all the information to display
    const outputText = `
        Unsubsidized Amount: ${unsubsidized} <br>
        Subsidized Amount: ${subsidized} <br>
        Interest Rate: ${interest}% <br>
        Monthly Payment: ${monthlyPayment}
    `;

    document.getElementById("output").innerHTML = outputText;
});


