#!/usr/bin/python3

#############################################################################################
#                               Program by Mohammed Faisal Khan                             #
#                               00598949                                                    #
#                               mkhan8@unh.newhaven.edu                                     #
#############################################################################################

# Importing system module
import sys
import re

# Function Definitions


# Function to check if the filename was given, if not ask the user to input file(s)
def check_files(filename):

    if not filename:
        print("File name not specified.")
        filename = input("Please enter name of data file(s): ")
        file_list = filename.split()
        return file_list
    else:
        return filename


# Function to read in the file contents if the file exists
def read_file(filename=""):

    # File exist error handling - http://www.diveintopython.net/file_handling/index.html
    try:
        current_file = open(filename, "r", encoding="utf8")
    except IOError:
        print("File does not exist.")
        return "Nothing to print."

    # Split lines - http://stackoverflow.com/questions/15233340/getting-rid-of-n-when-using-readlines
    content = current_file.read().splitlines()
    current_file.close()

    return content


# Printing function of the program
def print_expression(old, new, switch):

    if switch == 0:
        print("\nExpressions :", end="\n\n")
        for i in range(len(old)):
            print("Line ", i+1, ": ", old[i])
    else:
        if switch == 1:
            print("\nFirst Phase")
        elif switch == 2:
            print("\nSecond Phase")
        elif switch == 3:
            print("\nThird Phase")
        elif switch == 4:
            print("\nFinal Phase")

#        print(end="\n")

#        for expression in old:
#            if expression == '':
#                print("Expression not Valid!")
#            else:
#                print("Old Expression: ", expression)

        print(end="\n")

        i = 0

        for expression in new:
            i += 1
            if expression == '':
                print("Line", i, ": ", "Expression not valid!")
            else:
                print("Line", i, ": ", "New Expression: ", expression)

    print("\n#######################################################################################")


# Function to check if the expressions meet the requirement to be validated
def check_expression(not_validated, switch):

    validated = ""

#    print("\nNot validated: ", not_validated)
    temp_expression = not_validated.split()

    # Validation for the First Phase of the Program
    if switch == 1:
        for word in temp_expression:
            if word in {'opsub', 'opequal', 'opadd', 'opmult', 'oprdiv', 'opidiv',
                        'varint', 'varreal', 'litreal', 'litint'}:
                if len(validated) == 0:
                    validated += word
                else:
                    validated = validated + " " + word
    # Validation for the Second Phase of the Program
    elif switch == 2:
        for word in temp_expression:
            if word in {'opadd', 'opsub'}:
                validated = not_validated
                break
            elif word in {'varint', 'litint', 'litreal', 'opequal', 'termint', 'varreal', 'termreal'}:
                if len(validated) == 0:
                    validated += word
                else:
                    validated = validated + " " + word
    # Validation for the Third Phase of the Program
    elif switch == 3:
        for word in temp_expression:
            if word in {'subint', 'subreal', 'varint', 'litint', 'litreal',
                        'varreal', 'opequal', 'termint', 'termreal'}:
                if len(validated) == 0:
                    validated += word
                else:
                    validated = validated + " " + word
    elif switch == 4:
        for word in temp_expression:
            if word in {'statement'}:
                if len(validated) == 0:
                    validated += word
                else:
                    validated = validated + " " + word

#    print("Validated:", validated)

    # print("Length validated: ", len(validated))
    # print("Length not valid: ", len(not_validated))

    if len(validated) == len(not_validated):
        # print("Expression: Valid")
        return validated
    else:
        # print("Expression: Not Valid")
        return ''


# Substitution function for find_operand function
def var_sub(matchobj):

    match = matchobj.group(0)

    if match[0] == 'i':
        # print("Match for integer variable:", match)
        return 'varint'
    elif match[0] == 'r':
        # print("Match for real variable:   ", match)
        return 'varreal'


# Substitution function for find_operand function
def num_sub(matchobj):

    match = matchobj.group(0)

    if "." in match:
        # print("Match for literal real:   ", match)
        return 'litreal'
    else:
        # print("Match for literal integer:", match)
        return 'litint'


# Function to check the operands and convert them to terms appropriately
def find_operands(raw_expressions):

    var_expression = []
    new_expression = []

    variable = re.compile(r"[ir][a-zA-Z]+")
    number = re.compile(r"[-+]?([1-9][0-9]|[0-9])*[.]?[0-9]+")

    for expression in raw_expressions:
        var_expression.append(variable.sub(var_sub, expression))

    for expression in var_expression:
        new_expression.append(number.sub(num_sub, expression))

    print_expression(raw_expressions, new_expression, 1)

    return new_expression


# Substitution function for find_operator matches
def operator_sub(matchobj):

    match = matchobj.group(0)
#    print("Match :", match)

    if match[0] == '-':
        return 'opsub'
    elif match[0] == '+':
        return 'opadd'
    elif match[0] == '=':
        return 'opequal'
    elif match[0] == '*':
        return 'opmult'
    elif match[0] == '/':
        return 'oprdiv'
    elif match[0] == '//':
        return 'opidiv'


# Function to find all the operators and display them
def find_operators(operands_expression):

    operators_expression = []
    validated_expressions = []

    operators = re.compile(r"[-+=*/]/?")

    for expression in operands_expression:
        operators_expression.append(operators.sub(operator_sub, expression))

#    print_expression(operands_expression, operators_expression, 1)

    for expression in operators_expression:
        validated_expressions.append(check_expression(expression, 1))

#    print(validated_expressions)

    print_expression(operands_expression, validated_expressions, 1)

    return validated_expressions


# Substitution function for find_terms function
def term_sub(matchobj):

    match = matchobj.group(0)
#    print("\nMatch Term:", match)

    if match[0:6] in {'varint', 'litint'}:
        return 'termint'
    elif match[0:7] in {'varreal', 'litreal'}:
        return 'termreal'


# Function to find all terms and display them
def find_terms(phase_one):

    int_term = []
    real_term = []
    validated_expressions = []

    integer = re.compile(r"(var|lit)[int]+ ?[op]+(mult|idiv) ?(var|lit)[int]+")
    real = re.compile(r"(var|lit)[real]+ ?[op]+(mult|rdiv) ?(var|lit)[real]+")

    for expression in phase_one:
        int_term.append(integer.sub(term_sub, expression))

    for expression in int_term:
        real_term.append(real.sub(term_sub, expression))


#    print_expression(phase_one, real_term, 2)

    for expression in real_term:
        validated_expressions.append(check_expression(expression, 2))

#    print(validated_expressions)

    print_expression(phase_one, validated_expressions, 2)

    return validated_expressions


# Substitution function for find_expressions
def subexpression_sub(matchobj):

    match = matchobj.group(0)
#    print("\nMatch Subexpression:", match)

    if match[0:6] in {'varint', 'litint'}:
        return 'subint'
    elif match[0:7] in {'termint'}:
        return 'subint'
    elif match[0:7] in {'varreal', 'litreal'}:
        return 'subreal'
    elif match[0:8] in {'termreal'}:
        return 'subreal'


# Function to find all the subexpressions in a given expression
def find_subexpressions(phase_two):

    int_subexpression = []
    real_subexpression = []
    validated_expressions = []

    integer = re.compile(r"(var|lit|term)[int]+ ?[op]+(add|sub) ?(var|lit|term)[int]+")
    real = re.compile(r"(var|lit|term)[real]+ ?[op]+(add|sub) ?(var|lit|term)[real]+")

    for expression in phase_two:
        int_subexpression.append(integer.sub(subexpression_sub, expression))

    for expression in int_subexpression:
        real_subexpression.append(real.sub(subexpression_sub, expression))

#    print_expression(phase_two, real_subexpression, 3)

    for expression in real_subexpression:
        validated_expressions.append(check_expression(expression, 3))

#    print(validated_expressions)

    print_expression(phase_two, validated_expressions, 3)

    return validated_expressions


# Substitution function for Validation function
def valid_sub(matchobj):

    match = matchobj.group(0)
#    print("\nMatch Valid:", match)

    if match[0:6] == 'varint' or 'varreal':
        return 'statement'


# Function to do the final Validation of the expressions
def validation(phase_three):

    int_valid = []
    real_valid = []
    validated_expressions = []

    integer = re.compile(r"(([varint]+ ?[opequal]+ ?(var|lit|term|sub)[int]+)|"
                         r"([varreal]+ ?[opequal]+ ?(var|lit|term|sub)[real]+))")

    for expression in phase_three:
        int_valid.append(integer.sub(valid_sub, expression))

#    print_expression(phase_three, int_valid, 4)

    for expression in int_valid:
        validated_expressions.append(check_expression(expression, 4))

#    print(validated_expressions)

    print_expression(phase_three, validated_expressions, 4)

    return real_valid

#############################################################################################

# Main Program

# Command line argument to take names of files as input
files = sys.argv[1:]

files = check_files(files)
# print("Files: ", files)

# Loop to process multiple files
for file in files:
    print("\n###################################", file, "###################################", end="\n")
    statements = read_file(file)
    print_expression(statements, '', 0)

    replaced_operands = find_operands(statements)
#    print_expression(replaced_operands, '', 0)

    replaced_operators = find_operators(replaced_operands)
#    print_expression(replaced_operators, '', 0)

    replaced_terms = find_terms(replaced_operators)
#    print_expression(replaced_terms, '', 0)

    replaced_subexpressions = find_subexpressions(replaced_terms)
#    print_expression(replaced_subexpressions, '', 0)

    valid_statements = validation(replaced_subexpressions)
#    print(valid_statements)

#############################################################################################
#                                       End of Program                                      #
#############################################################################################
