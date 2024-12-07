import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.widgets import Button

class LoanAmortizationViewer:
    def __init__(self, df, rows_per_page=15):
        self.df = df
        self.rows_per_page = rows_per_page
        self.current_page = 0
        self.total_pages = int(np.ceil(len(df) / rows_per_page))
        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        plt.subplots_adjust(bottom=0.2)  # Adjust space for buttons
        
        # Create buttons
        self.ax_prev = plt.axes([0.3, 0.05, 0.1, 0.075])  # Position of "Previous" button
        self.ax_next = plt.axes([0.6, 0.05, 0.1, 0.075])  # Position of "Next" button
        self.btn_prev = Button(self.ax_prev, 'Previous')
        self.btn_next = Button(self.ax_next, 'Next')
        
        # Connect button events
        self.btn_prev.on_clicked(self.previous_page)
        self.btn_next.on_clicked(self.next_page)
        
        # Show the first page
        self.show_page()
        plt.show()
    
    def show_page(self):
        self.ax.clear()
        start_row = self.current_page * self.rows_per_page
        end_row = min((self.current_page + 1) * self.rows_per_page, len(self.df))
        df_page = self.df.iloc[start_row:end_row]
        
        # Create the table
        table = self.ax.table(cellText=df_page.values, colLabels=df_page.columns, cellLoc='center', loc='center')
        self.ax.axis('off')
        self.ax.set_title(f"Loan Amortization Schedule (Page {self.current_page + 1}/{self.total_pages})", fontsize=14)
        
        # Apply alternating row colors
        for i, key in enumerate(table.get_celld()):
            cell = table.get_celld()[key]
            if key[0] > 0:  # Avoid coloring header row
                if key[0] % 2 == 0:
                    cell.set_facecolor('#f0f0f0')  # Light gray for even rows
                else:
                    cell.set_facecolor('#ffffff')  # White for odd rows
        
        self.fig.canvas.draw()
    
    def next_page(self, event):
        if self.current_page < self.total_pages - 1:
            self.current_page += 1
            self.show_page()
    
    def previous_page(self, event):
        if self.current_page > 0:
            self.current_page -= 1
            self.show_page()

def loan_amortization(annual_interest_rate, loan_term_months, subsidized_amount, unsubsidized_amount, 
                      nonpayment_months, monthly_payment=None, target_months=None):
    # Calculate monthly interest rate
    principal = subsidized_amount + unsubsidized_amount
    monthly_interest_rate = annual_interest_rate / 12

    # Handle options for monthly payment or target months
    if monthly_payment is None and target_months is not None:
        # Calculate monthly payment for the given target months
        effective_rate = (1 + monthly_interest_rate) ** target_months
        monthly_payment = (principal * monthly_interest_rate * effective_rate) / (effective_rate - 1)
    elif monthly_payment is not None and target_months is None:
        pass
    else:
        raise ValueError("Specify either 'monthly_payment' or 'target_months', but not both.")

    # Initialize breakdown lists
    principal_remaining_subsidized = subsidized_amount
    principal_remaining_unsubsidized = unsubsidized_amount
    breakdown = []
    total_interest = 0
    total_paid = 0

    # Nonpayment period: Accrue interest only on unsubsidized loan
    for month in range(1, nonpayment_months + 1):
        interest_unsubsidized = principal_remaining_unsubsidized * monthly_interest_rate
        total_interest += interest_unsubsidized
        principal_remaining_unsubsidized += interest_unsubsidized

        breakdown.append({
            'Month': month,
            'Monthly Payment': 0,
            'Remaining Balance': round(principal_remaining_subsidized + principal_remaining_unsubsidized, 2),
            'Principal Paid': 0,
            'Total Paid': 0,
            'Monthly Interest': round(interest_unsubsidized, 2),
            'Total Interest': round(total_interest, 2)
        })

    # Combine subsidized and unsubsidized principals after the nonpayment period
    principal_remaining = principal_remaining_subsidized + principal_remaining_unsubsidized

    # Payment period: Pay off the loan
    max_months = 100 * 12  # Maximum allowed months (100 years)
    for month in range(nonpayment_months + 1, max_months + 1):
        
        interest_payment = principal_remaining * monthly_interest_rate
        total_interest += interest_payment

        
        principal_payment = min(monthly_payment - interest_payment, principal_remaining)  # Avoid overpaying
        principal_remaining -= principal_payment

        total_paid += (principal_payment + interest_payment)

        breakdown.append({
            'Month': month,
            'Monthly Payment': round(principal_payment + interest_payment, 2),
            'Remaining Balance': round(principal_remaining, 2),
            'Principal Paid': round(principal_payment, 2),
            'Total Paid': round(total_paid, 2),
            'Monthly Interest': round(interest_payment, 2),
            'Total Interest': round(total_interest, 2)
        })

        # Stop if loan is paid off
        if principal_remaining <= 0:
            break

    if principal_remaining > 0:
        print("Loan could not be paid off within the 100-year limit.")
        return

    # Convert to DataFrame
    df = pd.DataFrame(breakdown)

    # Initialize the viewer
    LoanAmortizationViewer(df)

# Example usage for fixed monthly payment
loan_amortization(
    annual_interest_rate=0.06,
    loan_term_months=120,
    subsidized_amount=00000,
    unsubsidized_amount=25000,
    nonpayment_months=0,
    monthly_payment=1000
)

# Example usage for target months
loan_amortization(
    annual_interest_rate=0.06,
    loan_term_months=120,
    subsidized_amount=0000,
    unsubsidized_amount=25000,
    nonpayment_months=0,
    target_months=36  # Pay off in 180 months
)
