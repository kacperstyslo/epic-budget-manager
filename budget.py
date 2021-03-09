import os
import sys
import time
from dataclasses import dataclass
from typing import Dict
from tkinter.simpledialog import askfloat


@dataclass
class BudgetMain:
    budget_value: float = 0.0
    savings: float = 0.0
    expenses: float = 0.0

    def __init__(self):
        self.savings_expense_over_time: Dict[str, float] = {}

    def __call__(self):
        return self.budget_value

    def add_income_to_budget(self):
        current_income = askfloat("Income", "Bellow add current income")
        self.savings += current_income
        self.budget_value += current_income
        current_date = self.get_current_time()
        self.savings_expense_over_time[str(current_date)] = self.savings
        self.save_data_and_values_into_file(date=current_date, value=self.savings)
        del self.savings
        os.execv(sys.executable, ['python3'] + [os.path.basename(__file__)]) if os.name != 'nt' else os.execv(sys.executable, ['python'] + [sys.argv[0]])

    def add_expense_to_budget(self):
        current_expense = askfloat("Expense", "Bellow add current expense")
        self.expenses -= current_expense
        self.budget_value -= current_expense
        current_date = str(self.get_current_time())
        self.savings_expense_over_time[current_date] = self.expenses
        self.save_data_and_values_into_file(date=current_date, value=self.expenses)
        del self.expenses
        os.execv(sys.executable, ['python3'] + [os.path.basename(__file__)]) if os.name != 'nt' else os.execv(sys.executable, ['python'] + [sys.argv[0]])

    @staticmethod
    def get_current_time():
        current_time = time.time()
        return current_time

    @staticmethod
    def save_data_and_values_into_file(date, value):
        file_name = 'expenses.csv'
        if value > 0:
            file_name = 'savings.csv'
        with open(f'{file_name}', 'a') as fa:
            fa.write(f'{date}|{value}\n')
