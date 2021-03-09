#!/usr/bin/env python3

import sys
from charts import ChartsMain


class Main:
    def __init__(self):
        self.charts_main = ChartsMain()

    def start_up(self):
        self.charts_main()

    @staticmethod
    def say_goodbye():
        print('Exit...')
        sys.exit(0)


if __name__ == '__main__':
    Main().start_up()

# VERSION 1.1
