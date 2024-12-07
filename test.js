// This would NOT work if called before the function is declared
calculateLoanAmortization(1000);

const calculateLoanAmortization = function(amount) {
    console.log(amount);
};

// This works because of hoisting
calculateLoanAmortization(1000);

function calculateLoanAmortization(amount) {
    console.log(amount);
}


