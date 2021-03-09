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
        self.root.geometry("900x1080")

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
        savings_dates_for_graph_converted = [datetime.fromtimestamp(float(d)).strftime("%Y/%m/%d") for d in savings_dates_for_graph]
        savings_s_l_fig = plt.Figure(figsize=(5, 6), dpi=100)
        savings_s_l_ax = savings_s_l_fig.add_subplot(111)
        savings_s_l = FigureCanvasTkAgg(savings_s_l_fig, self.root)
        savings_s_l.get_tk_widget().pack(side=LEFT, anchor=NW)
        savings_s_l_ax.plot(savings_dates_for_graph_converted, kwargs['savings_values_for_graph'], marker='o', color='green', linewidth=2)
        savings_s_l_ax.set_title('Savings 2021')
        savings_s_l_ax.set_ylim(ymin=0)
        savings_s_l_ax.yaxis.grid()
        savings_s_l_fig.tight_layout()

    def draw_data_table(self, data_for_table: list):
        data_table_fig = plt.Figure(figsize=(10.8, 4), dpi=100)
        data_table_ax = data_table_fig.subplots()
        data_table = FigureCanvasTkAgg(data_table_fig, self.root)
        data_table.get_tk_widget().place(relx=0.48, rely=0.75, anchor=CENTER)
        dt = pd.DataFrame(np.array(data_for_table), columns=list(['Cash movement', 'Dates']))
        data_table_fig.patch.set_visible(False)
        data_table_ax.axis('off')
        data_table_ax.axis('tight')
        data_table_ax.table(cellText=dt.values, colLabels=dt.columns, loc='center')

    def draw_pie_chart(self, **kwargs: list):
        pie_fig = plt.Figure(figsize=(4, 6), dpi=100)
        pie_ax = pie_fig.subplots()
        pie_obj = FigureCanvasTkAgg(pie_fig, self.root)
        pie_obj.get_tk_widget().pack(side=LEFT, anchor=NE)
        pie_values = [sum(kwargs['savings_values_for_graph']), sum(kwargs['expenses_values_for_graph']) * (-1)]
        pie_ax.pie(pie_values, labels=('Savings', 'Expense'), autopct='%1.1f%%', colors=['green', 'red'], startangle=90)
        pie_ax.axis('equal')
        pie_ax.set_title('Budget 2021')

    def show_savings_and_expenses_buttons(self):
        buttons_font_size = font.Font(size=25)
        savings_button = Button(self.root, command=self.add_income_to_budget, text='+', width=25, bg='#00cc00', fg='#ffffff')
        expenses_button = Button(self.root, command=self.add_expense_to_budget, text='-', width=25, bg='#FF0000', fg='#ffffff')
        savings_button.place(x=0, y=950)
        expenses_button.place(x=450, y=950)
        savings_button['font'], expenses_button['font'] = buttons_font_size, buttons_font_size

    def draw_elements(self, **kwargs: list):
        self.draw_savings_single_line_chart(savings_values_for_graph=kwargs[f'savings_values_for_graph'], savings_dates_for_graph=kwargs['savings_dates_for_graph'])
        self.draw_data_table(data_for_table=kwargs['data_for_table'])
        self.show_savings_and_expenses_buttons()
        self.draw_pie_chart(savings_values_for_graph=kwargs['savings_values_for_graph'], expenses_values_for_graph=kwargs['expenses_values_for_graph'])
        self.root.mainloop()
