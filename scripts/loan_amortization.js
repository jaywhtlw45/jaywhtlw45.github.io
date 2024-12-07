document.getElementById("calculate").addEventListener("click", function () {
    const principal = parseFloat(document.getElementById("principal)").value);
    const interestRate = parseFloat(document.getElementById("interest").value) / 100;
    const monthlyPayment = parseFloat(document.getElementById("monthlyPayment")).value;
    const subsidized = parseFloat(document.getElementById("subsidized").value);

    if (isNaN(principal) || isNaN(intersestRate) || isNaN(monthlyPayment) || isNaN(subsidized)){
        document.getElementById("output").innerText="Please fill in all fields";
        return;
    }

    const results = calculateLoanAmortization(principal, interstRate, monthlyPament, subsidized);
    document.getElementById("output").innerHTML = JSON.stringify(results, null, 2);

    function calculateLoanAmortization(principal, interestaRate, monthlyPayment, subsidized){
        return[];
    }
});


