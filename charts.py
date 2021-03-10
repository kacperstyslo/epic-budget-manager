import os
import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tkinter.font as font
from tkinter import *
from datetime import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from budget import BudgetMain


class ChartsMain(BudgetMain):
    def __init__(self):
        super().__init__()
        self.file_names: list = ['savings.csv', 'expenses.csv']
        self.root = Tk(className="Epic Budget Manager")
        self.root.geometry('1920x1080')
        self.root.configure(background='white')
        self.root.resizable(width=False, height=False)

    def __call__(self):
        try:
            savings_values, savings_dates = self.collecting_data_for_charts(self.file_names[0], values=[], date=[])
            expenses_values, expenses_dates = self.collecting_data_for_charts(self.file_names[1], values=[], date=[])
        except FileNotFoundError:
            self.save_data_and_values_into_file(self.get_current_time(), 1)
            self.save_data_and_values_into_file(self.get_current_time(), -1)
            os.execv(sys.executable, ['python3'] + [os.path.basename(__file__)]) if os.name != 'nt' else os.execv(sys.executable, ['python'] + [sys.argv[0]])
        else:
            data_for_table = self.converting_data_for_graph_table(savings_data_for_last_five_entries=dict(zip(savings_dates[-5:], savings_values[-5:])),
                                                                  expenses_data_for_last_five_entries=dict(zip(expenses_dates[-5:], expenses_values[-5:])))
            summed_savings_values = self.converting_data_for_charts(savings_values, summed_values_list=[])
            summed_expenses_values = self.converting_data_for_charts(expenses_values, summed_values_list=[])
            self.draw_elements(savings_values_for_graph=summed_savings_values,
                               savings_dates_for_graph=savings_dates,
                               expenses_values_for_graph=summed_expenses_values,
                               data_for_table=data_for_table)

    @staticmethod
    def collecting_data_for_charts(file_name: str, values: list, date: list):
        with open(f'{file_name}', 'r') as fr:
            file = csv.reader(fr, dialect='excel', delimiter='|')
            for data in file:
                date.append(data[0]), values.append(float(data[1]))
        return values, date

    @staticmethod
    def converting_data_for_charts(values: list, summed_values_list: list):
        for count, value in enumerate(values, 1):
            count_list = [count]
            for v in range(len(count_list)):
                summed_values_list.append(sum(values[:count]))
        return summed_values_list

    @staticmethod
    def converting_data_for_graph_table(savings_data_for_last_five_entries: dict, expenses_data_for_last_five_entries: dict):
        last_five_entries = []
        last_five_entries.extend([(s_d, s_v) for s_d, s_v in savings_data_for_last_five_entries.items()])
        last_five_entries.extend([(e_d, e_v) for e_d, e_v in expenses_data_for_last_five_entries.items()])
        while len(last_five_entries) > 5:
            last_five_entries.remove(min(last_five_entries))
        last_five_entries = sorted(last_five_entries, reverse=True)
        last_five_entries_formatted = [(datetime.fromtimestamp(float(d)).strftime("%Y/%m/%d"), v) for d, v in last_five_entries]
        return last_five_entries_formatted

    def draw_savings_single_line_chart(self, **kwargs: list):
        savings_dates_for_graph = kwargs['savings_dates_for_graph']
        savings_dates_for_graph_converted = [datetime.fromtimestamp(float(d)).strftime("%y/%m/%d") for d in savings_dates_for_graph]
        savings_single_line_fig = plt.Figure(figsize=(6, 6.8), dpi=100)
        savings_single_line_ax = savings_single_line_fig.add_subplot(111)
        savings_single_line = FigureCanvasTkAgg(savings_single_line_fig, self.root)
        savings_single_line.get_tk_widget().place(relx=.15, rely=.32, anchor=CENTER)
        savings_single_line_ax.plot(savings_dates_for_graph_converted, kwargs['savings_values_for_graph'], marker='o', color='green', linewidth=2)
        savings_single_line_ax.set_title('Savings 2021')
        savings_single_line_ax.set_ylim(ymin=0)
        savings_single_line_ax.yaxis.grid()
        savings_single_line_fig.tight_layout()

    def draw_pie_chart(self, **kwargs: list):
        pie_fig = plt.Figure(figsize=(8, 6), dpi=100)
        pie_ax = pie_fig.subplots()
        pie_obj = FigureCanvasTkAgg(pie_fig, self.root)
        pie_obj.get_tk_widget().place(relx=.5, rely=.3, anchor=CENTER)
        pie_values = [sum(kwargs['savings_values_for_graph']), sum(kwargs['expenses_values_for_graph']) * (-1)]
        pie_ax.pie(pie_values, labels=('Savings', 'Expense'), autopct='%1.1f%%', colors=['green', 'red'], startangle=90)
        pie_ax.axis('equal')
        pie_ax.set_title('Budget 2021')

    def draw_savings_expenses_bar_chart(self, savings_values_bar_chart, expenses_values_for_bar_chart):
        bar_savings_expenses_fig = plt.Figure(figsize=(6, 8), dpi=100)
        bar_savings_expenses_ax = bar_savings_expenses_fig.subplots()
        bar_savings_expenses = FigureCanvasTkAgg(bar_savings_expenses_fig, self.root)
        bar_savings_expenses.get_tk_widget().place(relx=.85, rely=.31, anchor=CENTER)
        bar_savings_expenses_ax.set_title("Savings & Expenses")
        bar_savings_expenses_ax.axhline(y=0, linewidth=2, color='k')
        bar_savings_expenses_ax.bar('Savings', sum(savings_values_bar_chart), width=0.1, label='Savings', color='green')
        bar_savings_expenses_ax.bar('Expenses', sum(expenses_values_for_bar_chart), width=0.1, label='Expenses', color='red')

    def draw_data_table(self, data_for_table: list):
        data_table_fig = plt.Figure(figsize=(9, 2), dpi=100)
        data_table_ax = data_table_fig.subplots()
        data_table = FigureCanvasTkAgg(data_table_fig, self.root)
        data_table.get_tk_widget().place(relx=.5, rely=.7, anchor=CENTER)
        dt = pd.DataFrame(np.array(data_for_table), columns=list(['Dates', 'Value']))
        data_table_fig.patch.set_visible(False)
        data_table_ax.axis('off')
        data_table_ax.axis('tight')
        data_table_ax.set_title("Latest Revenue and Expenses", fontweight="bold", color='red')
        data_table_ax.table(cellText=dt.values, colLabels=dt.columns, loc='center', colColours=["yellow"] * 2)

    def show_savings_and_expenses_buttons(self):
        buttons_font_size = font.Font(size=25)
        savings_button = Button(self.root, command=self.add_income_to_budget, text='+', width=26, bg='#00cc00', fg='#ffffff')
        expenses_button = Button(self.root, command=self.add_expense_to_budget, text='-', width=26, bg='#FF0000', fg='#ffffff')
        savings_button.place(x=450, y=950)
        expenses_button.place(x=950, y=950)
        savings_button['font'], expenses_button['font'] = buttons_font_size, buttons_font_size

    def draw_elements(self, **kwargs: list):
        self.show_savings_and_expenses_buttons()
        self.draw_data_table(data_for_table=kwargs['data_for_table'])
        self.draw_pie_chart(savings_values_for_graph=kwargs['savings_values_for_graph'], expenses_values_for_graph=kwargs['expenses_values_for_graph'])
        self.draw_savings_single_line_chart(savings_values_for_graph=kwargs[f'savings_values_for_graph'], savings_dates_for_graph=kwargs['savings_dates_for_graph'])
        self.draw_savings_expenses_bar_chart(savings_values_bar_chart=kwargs['savings_values_for_graph'], expenses_values_for_bar_chart=kwargs['expenses_values_for_graph'])
        self.root.mainloop()
