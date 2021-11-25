## Code taken from: https://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console

import os

class ProgressBar:

    def __init__(self, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '@', printEnd = "\r"):
        self.count = 1
        self.total = total
        self.prefix = prefix
        self.suffix = suffix
        self.decimals = decimals
        self.length = length
        self.fill = fill
        self.printEnd = printEnd

    def printProgressBar (self):
        """
        Call in a loop to create terminal progress bar
        @params:
            iteration   - Required  : current iteration (Int)
            total       - Required  : total iterations (Int)
            prefix      - Optional  : prefix string (Str)
            suffix      - Optional  : suffix string (Str)
            decimals    - Optional  : positive number of decimals in percent complete (Int)
            length      - Optional  : character length of bar (Int)
            fill        - Optional  : bar fill character (Str)
            printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
        """
        os.system('cls')

        percent = ("{0:." + str(self.decimals) + "f}").format(100 * (self.count / float(self.total)))
        filledLength = int(self.length * self.count // self.total)
        bar = self.fill * filledLength + '-' * (self.length - filledLength)
        print(f'\r{self.prefix} |{bar}| {percent}% {self.suffix}', end = self.printEnd)
        self.count = self.count + 1
        # Print New Line on Complete
        if self.count == self.total: 
            print()