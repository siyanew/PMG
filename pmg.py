import re
import os


class PMG:
    def __init__(self, file):
        self.file = file
        self.writer = Writer()
        self.parse = Parser(self.writer)

    def read(self):
        line_counter = 0
        with open(self.file) as f:
            for line in f:
                line_counter += 1
                self.parse.parse(line, line_counter)
        self.writer.endfile()
        os.system('python run.py')


class Parser:
    def __init__(self,writer):
        self.varCounter = 0
        self.varList = []
        self.writer = writer

    def parse(self, string, linenum):
        if re.match("([a-zA-z][a-zA-z1-9]*?)\s*=\s*([a-zA-z][a-zA-z]*?)\s*\+\s*1", string):
            tokens = re.findall("([a-zA-z][a-zA-z1-9]*?)\s*=\s*([a-zA-z][a-zA-z]*?)\s*\+\s*1", string)
            self.writer.write('var_search("' + tokens[0][0] + '").plus()')

        elif re.match("([a-zA-z]?[a-zA-z1-9]*)\s*=\s*([a-zA-z]?[a-zA-z]*)\s*-\s*1", string):
            tokens = re.findall("([a-zA-z][a-zA-z1-9]*?)\s*=\s*([a-zA-z][a-zA-z]*?)\s*-\s*1", string)
            self.writer.write('var_search("' + tokens[0][0] + '").minus()')
        elif re.match("([a-zA-z]?[a-zA-z1-9]*)\s*:\s*([a-zA-z][a-zA-z]*?)\s*=\s*([a-zA-z][a-zA-z]*?)\s*\+\s*1", string):
            tokens = re.findall(
                "([a-zA-z]?[a-zA-z1-9]*)\s*:\s*([a-zA-z][a-zA-z]*?)\s*=\s*([a-zA-z][a-zA-z]*?)\s*\+\s*1", string)
            self.writer.write('label .' + tokens[0][0])
            self.writer.write('var_search("' + tokens[0][1] + '").plus()')
        elif re.match("([a-zA-z]?[a-zA-z1-9]*)\s*:\s*([a-zA-z][a-zA-z]*?)\s*=\s*([a-zA-z][a-zA-z]*?)\s*-\s*1", string):
            tokens = re.findall("([a-zA-z]?[a-zA-z1-9]*)\s*:\s*([a-zA-z][a-zA-z]*?)\s*=\s*([a-zA-z][a-zA-z]*?)\s*-\s*1",
                                string)
            self.writer.write('label .' + tokens[0][0])
            self.writer.write('var_search("' + tokens[0][1] + '").minus()')
        elif re.match("if\s+([a-zA-z]?[a-zA-z1-9]*)\s*!=\s*0\s+goto\s+([a-zA-z]?[a-zA-z1-9]*)", string):
            tokens = re.findall("if\s+([a-zA-z]?[a-zA-z1-9]*)\s*!=\s*0\s+goto\s+([a-zA-z]?[a-zA-z1-9]*)", string)
            self.writer.write('if var_search("' + tokens[0][0] + '").num != 0:')
            self.writer.write('    goto .' + tokens[0][1])
        elif re.match(
                "([a-zA-z]?[a-zA-z1-9]*)\s*:\s*if\s+([a-zA-z]?[a-zA-z1-9]*)\s*!=\s*0\s+goto\s+([a-zA-z]?[a-zA-z1-9]*)",
                string):
            tokens = re.findall(
                "([a-zA-z]?[a-zA-z1-9]*)\s*:\s*if\s+([a-zA-z]?[a-zA-z1-9]*)\s*!=\s*0\s+goto\s+([a-zA-z]?[a-zA-z1-9]*)",
                string)
            self.writer.write('label .' + tokens[0][0])
            self.writer.write('if var_search("' + tokens[0][1] + '").num != 0:')
            self.writer.write('    goto .' + tokens[0][2])

        else:
            print("There is an error in line : " + str(linenum))


class Writer:
    def __init__(self):
        self.file = open("run.py", "w")
        self.file.write("""from goto import goto, label

varList=[]


class Variable:
    def __init__(self,name):
        self.num = int(raw_input("Enter " + name + " Value :"))
        self.name = name

    def plus(self):
        self.num += 1
        print_var()

    def minus(self):
        if self.num != 0:
            self.num -= 1
        print_var()


def print_var():
    for var in varList:
        print var.name + " = " + str(var.num) + "\t" ,
    print ""


def var_search(name):
    for var in varList:
        if var.name == name:
            return var
    var = Variable(name)
    varList.append(var)
    return var


def run():
""")

    def write(self, string):
        self.file.write("    " + string + "\n")

    def endfile(self):
        self.file.write("""

run()
""")
        self.file.close()
