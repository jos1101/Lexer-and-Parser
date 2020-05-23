"""
James Smith
COP4620
Spring 2019
Project 2

This is my implementation of a LL(1) recursive decent parser for the C- language.
"""
import inspect
import sys
import re


def is_keyword(st):
    """Keywords"""
    return st == "int" or st == "float" or st == "void" or st == "return" or st == "if" or st == "else" or st == "while"


def is_rel_op(st):
    """Relational Operators"""
    return st == "=" or st == "==" or st == "!=" or st == "<" or st == ">" or st == "<=" or st == ">="


def is_math_op(ch):
    """Math Operations"""
    return ch == "+" or ch == "-" or ch == "/" or ch == "*"


def is_delimiter(st):
    """Delimiters"""
    return st == "," or st == " " or st == ";" or st == "(" or st == ")" \
           or st == "[" or st == "]" or st == "{" or st == "}" or st == ","


def is_num(st):
    """Floats and integers"""
    x = re.search("^(\d+(\.\d+)?([E][-+]?\d+)?)$", st)
    if x:
        return True
    else:
        return False
    # return re.search("^(\d+(\.\d+)?([E][-+]?\d+)?)$", st)


def compile_chlist(char_list):
    """If there are elements in the list, check for valid tokens, then delete the list for reuse"""
    word = ''.join(char_list)
    if char_list:
        if is_keyword(word):
            # print "KEYWORD:", word
            tokens.append(word)
        elif word.isalpha():
            # print"ID:", word
            tokens.append(word)
        elif is_num(word):
            # print "NUM:", word
            tokens.append(word)
        elif is_rel_op(word):
            # print "RELOP:", word
            tokens.append(word)
        else:
            # print "ERROR:", word'
            print "REJECT"
            sys.exit()
        del char_list[:]


def append_and_compile(char, char_list):
    """append the list, compile the lexemes to be checked"""
    char_list.append(char)
    compile_chlist(char_list)



def reject():
    """reject function with commented out operations for debugging purposes"""
    '''curframe = inspect.currentframe()
    calframe = inspect.getouterframes(curframe, 2)
    print('caller name:', calframe[1][3])
    print tokens'''
    print "REJECT"
    sys.exit()


def watch_decent():
    """a method used to track the decent for debugging"""
    '''curframe = inspect.currentframe()
    calframe = inspect.getouterframes(curframe, 2)
    print('caller name:', calframe[1][3])
    print tokens[-1]
    watch_decent.counter += 1'''
    pass


def valid_id(word):
    """valid id check"""
    return word.isalpha() and not is_keyword(word)

code = []
temp_code = []
type = None
id = None

def parser():
    """begin parsing"""
    watch_decent()
    program()


def program():
    watch_decent()
    if tokens[-1] == 'int' or tokens[-1] == 'void' or tokens[-1] == 'float':
        declaration_list()
    else:
        reject()


def declaration_list():
    watch_decent()
    if tokens[-1] == 'int' or tokens[-1] == 'void' or tokens[-1] == 'float':
        declaration()
        declaration_list_prime()
    else:
        reject()


def declaration_list_prime():
    watch_decent()
    if tokens[-1] == 'int' or tokens[-1] == 'void' or tokens[-1] == 'float':
        declaration()
        declaration_list_prime()
    elif tokens[-1] == '$':
        return
    else:
        reject()


def declaration():
    watch_decent()
    type_specifier()
    if valid_id(tokens[-1]):
        id = tokens.pop()
        declaration_prime()
    else:
        reject()


def declaration_prime():
    if tokens[-1] == '(':
        fun_declaration()
    elif tokens[-1] == '[' or tokens[-1] == ';':
        var_declaration_prime()
    else:
        reject()


def var_declaration():
    watch_decent()
    type_specifier()
    if valid_id(tokens[-1]):
        tokens.pop()
        var_declaration_prime()
    else:
        reject()


def var_declaration_prime():
    watch_decent()
    if tokens[-1] == ';':
        tokens.pop()
    elif tokens[-1] == '[':
        tokens.pop()
        if tokens[-1].isdigit():
            tokens.pop()
            if tokens[-1] == ']':
                tokens.pop()
                if tokens[-1] == ';':
                    tokens.pop()
                else:
                    reject()
            else:
                reject()
        else:
            reject()
    else:
        reject()


def type_specifier():
    watch_decent()
    if tokens[-1] == 'void' or tokens[-1] == 'float' or tokens[-1] == 'int':
        type = tokens.pop()  # accept
    else:
        reject()


def fun_declaration():
    watch_decent()
    if tokens[-1] == '(':
        tokens.pop()
        params()
        if tokens[-1] == ')':
            tokens.pop()
            compound_stmt()
        else:
            reject()
    else:
        reject()


def params():
    watch_decent()
    if tokens[-1] == 'void':
        temp_code.append("func")
        temp_code.append(id)
        temp_code.append("0")
        tokens.pop()
    elif tokens[-1] == 'float' or tokens[-1] == 'int':
        param_list()
    else:
        reject()


def param_list():
    watch_decent()
    if tokens[-1] == 'int' or tokens[-1] == 'void' or tokens[-1] == 'float':
        param()
        param_list_prime()
    else:
        reject()


def param_list_prime():
    watch_decent()
    if tokens[-1] == ',':
        tokens.pop()  # accept ,
        param()
        param_list_prime()
    elif tokens[-1] == ')':
        return
    else:
        reject()


def param():
    watch_decent()
    if tokens[-1] == 'int' or tokens[-1] == 'void' or tokens[-1] == 'float':
        tokens.pop()
        if valid_id(tokens[-1]):
            tokens.pop()
            param_prime()
        else:
            reject()
    else:
        reject()


def param_prime():
    watch_decent()
    if tokens[-1] == '[':
        tokens.pop()  # accept [
        if tokens[-1] == ']':
            tokens.pop()  # accept ]
        else:
            reject()
    elif tokens[-1] == ')' or tokens[-1] == ',':
        return
    else:
        reject()


def compound_stmt():
    watch_decent()
    if tokens[-1] == '{':
        tokens.pop()  # accept {
        local_declarations()
        statement_list()
        if tokens[-1] == '}':
            tokens.pop()
        else:
            reject()
    else:
        reject()


def local_declarations():
    watch_decent()
    if tokens[-1] == 'void' or tokens[-1] == 'float' or tokens[-1] == 'int':
        local_declarations_prime()
    elif tokens[-1] == '(' or valid_id(tokens[-1]) or tokens[-1] == ';' or is_num(tokens[-1]) or tokens[
        -1] == 'if' or tokens[-1] == 'return' or tokens[-1] == 'while' or tokens[-1] == '{' or tokens[-1] == '}':
        local_declarations_prime()
    else:
        reject()


def local_declarations_prime():
    watch_decent()
    if tokens[-1] == 'void' or tokens[-1] == 'float' or tokens[-1] == 'int':
        var_declaration()
        local_declarations_prime()
    elif tokens[-1] == '(' or valid_id(tokens[-1]) or tokens[-1] == ';' or is_num(tokens[-1]) or tokens[
        -1] == 'if' or tokens[-1] == 'return' or tokens[-1] == 'while' or tokens[-1] == '{' or tokens[-1] == '}':
        return
    else:
        reject()


def statement_list():
    watch_decent()
    if tokens[-1] == '(' or valid_id(tokens[-1]) or tokens[-1] == ';' or is_num(tokens[-1]) or tokens[
        -1] == 'if' or tokens[-1] == 'return' or tokens[-1] == 'while' or tokens[-1] == '{':
        statement_list_prime()
    elif tokens[-1] == '}':
        statement_list_prime()
    else:
        reject()


def statement_list_prime():
    watch_decent()
    if valid_id(tokens[-1]) or tokens[-1] == '{' or tokens[-1] == 'if' or tokens[-1] == 'while' or tokens[
        -1] == 'return' or is_num(tokens[-1]) or tokens[-1] == '(':
        statement()
        statement_list()
    elif tokens[-1] == '}':
        return
    else:
        reject()


def statement():
    watch_decent()
    if valid_id(tokens[-1]) or tokens[-1] == '(' or tokens[-1] == ';' or is_num(tokens[-1]):
        expression_statement()
    elif tokens[-1] == '{':
        tokens.pop()
        local_declarations()
        statement_list()
        if tokens[-1] == '}':
            tokens.pop()
        else:
            reject()
    elif tokens[-1] == 'if':
        selection_statement()
    elif tokens[-1] == 'while':
        iteration_statement()
    elif tokens[-1] == 'return':
        return_statement()
    else:
        reject()


def expression_statement():
    watch_decent()
    if tokens[-1] == ';':
        tokens.pop()
    elif tokens[-1] == '(' or valid_id(tokens[-1]) or is_num(tokens[-1]):
        expression()
        if tokens[-1] == ';':
            tokens.pop()
        else:
            # print "expression_statement else"
            reject()
    else:
        reject()


def selection_statement():
    watch_decent()
    if tokens[-1] == 'if':
        tokens.pop()
        if tokens[-1] == '(':
            tokens.pop()
            expression()
            if tokens[-1] == ')':
                tokens.pop()
                statement()
                selection_statement_prime()
            else:
                reject()
        else:
            reject()
    else:
        reject()


def selection_statement_prime():
    watch_decent()
    if tokens[-1] == 'else':
        tokens.pop()
        statement()
    elif tokens[-1] == '(' or valid_id(tokens[-1]) or tokens[-1] == ';' or is_num(tokens[-1]) or tokens[
        -1] == 'if' or tokens[-1] == 'return' or tokens[-1] == "else" or tokens[-1] == 'while' or tokens[-
    1] == '{' or tokens[-1] == '}':
        return
    else:
        reject()


def iteration_statement():
    watch_decent()
    if tokens[-1] == 'while':
        tokens.pop()
        if tokens[-1] == '(':
            tokens.pop()
            expression()
            if tokens[-1] == ')':
                tokens.pop()
                statement()
            else:
                reject()
        else:
            reject()
    else:
        reject()


def return_statement():
    watch_decent()
    if tokens[-1] == 'return':
        tokens.pop()
        return_statement_prime()
    else:
        reject()


def return_statement_prime():
    watch_decent()
    if tokens[-1] == ';':
        tokens.pop()
    elif valid_id(tokens[-1]):
        tokens.pop()
        return_statement_prime_prime_prime()
    elif tokens[-1] == '(':
        tokens.pop()
        expression()
        if tokens[-1] == ')':
            tokens.pop()
            term_prime()
            additive_expression_prime()
            simple_expression_prime()
            if tokens[-1] == ';':
                tokens.pop()
            else:
                reject()
        else:
            reject()
    elif is_num(tokens[-1]):
        tokens.pop()
        term_prime()
        additive_expression_prime()
        simple_expression_prime()
        if tokens[-1] == ';':
            tokens.pop()
        else:
            reject()
    else:
        reject()


def return_statement_prime_prime():
    watch_decent()
    if tokens[-1] == '=':
        tokens.pop()
        expression()
        if tokens[-1] == ';':
            tokens.pop()
        else:
            reject()
    else:
        term_prime()
        additive_expression_prime()
        simple_expression_prime()
        if tokens[-1] == ';':
            tokens.pop()
        else:
            reject()


def return_statement_prime_prime_prime():
    watch_decent()
    if tokens[-1] == '(':
        tokens.pop()
        args()
        if tokens[-1] == ')':
            tokens.pop()
            term_prime()
            additive_expression_prime()
            simple_expression_prime()
            if tokens[-1] == ';':
                tokens.pop()
            else:
                reject()
    else:
        var_prime()
        return_statement_prime_prime()


def expression():
    watch_decent()
    if valid_id(tokens[-1]) and tokens[-2] != '(':
        tokens.pop()
        var_prime()
        if tokens[-1] == '=':
            tokens.pop()
            expression()
        elif is_rel_op(tokens[-1]) and tokens[-1] != '=':
            simple_expression_prime()
        elif tokens[-1] == '+' or tokens[-1] == '-':
            additive_expression_prime()
        elif tokens[-1] == '*' or tokens[-1] == '*':
            term_prime()
        elif tokens[-1] == ')' or tokens[-1] == ',' or tokens[-1] == ';' or tokens[-1] == ']':
            return
        else:
            reject()
    elif tokens[-1] == '(' or is_num(tokens[-1]) or valid_id(tokens[-1]):
        simple_expression()
    else:
        reject()


def var():
    watch_decent()
    if valid_id(tokens[-1]):
        tokens.pop()
        var_prime()
    else:
        reject()


def var_prime():
    watch_decent()
    if tokens[-1] == '[':
        tokens.pop()
        expression()
        if tokens[-1] == ']':
            tokens.pop()
        else:
            reject()
    elif is_rel_op(tokens[-1]) or tokens[-1] == ')' or is_math_op(tokens[-1]) or tokens[
        -1] == ';' or tokens[-1] == ']' or tokens[-1] == ',':
        return
    else:
        reject()


def simple_expression():
    watch_decent()
    if tokens[-1] == '(' or valid_id(tokens[-1]) or is_num(tokens[-1]):
        additive_expression()
        simple_expression_prime()
    else:
        # print "simple_expression()"
        reject()


def simple_expression_prime():
    watch_decent()
    if is_rel_op(tokens[-1]) and tokens[-1] != '=':
        tokens.pop()
        additive_expression()
    elif tokens[-1] == ')' or tokens[-1] == ',' or tokens[-1] == ';' or tokens[-1] == ']':
        return
    else:
        reject()


def relop():
    watch_decent()
    if is_rel_op(tokens[-1]) and tokens[-1] != '=':
        tokens.pop()
    else:
        reject()


def additive_expression():
    watch_decent()
    if tokens[-1] == '(' or valid_id(tokens[-1]) or is_num(tokens[-1]):
        term()
        additive_expression_prime()
    else:
        reject()


def additive_expression_prime():
    watch_decent()
    if tokens[-1] == '+' or tokens[-1] == '-':
        addop()
        term()
        additive_expression_prime()
    elif is_rel_op(tokens[-1]) or tokens[-1] == ')' or tokens[-1] == ',' or tokens[-1] == ';' or tokens[-1] == ']':
        return ()
    else:
        return


def addop():
    watch_decent()
    if tokens[-1] == '+' or tokens[-1] == '-':
        tokens.pop()
    else:
        reject()


def term():
    watch_decent()
    if tokens[-1] == '(' or valid_id(tokens[-1]) or is_num(tokens[-1]):
        factor()
        term_prime()
    else:
        reject()


def term_prime():
    watch_decent()
    if tokens[-1] == '*' or tokens[-1] == '/':
        mulop()
        factor()
        term_prime()
    elif (is_rel_op(tokens[-1]) and tokens[-1] != '=') or tokens[-1] == ')' or tokens[-1] == ',' or tokens[-
    1] == ';' or tokens[-1] == ']' or tokens[-1] == '+' or tokens[-1] == '-':
        return
    else:
        reject()


def mulop():
    watch_decent()
    if tokens[-1] == '*' or tokens[-1] == '/':
        tokens.pop()
    else:
        reject()


def factor():
    watch_decent()
    if tokens[-1] == '(':
        tokens.pop()
        expression()
        if tokens[-1] == ')':
            tokens.pop()
        else:
            reject()
    elif valid_id(tokens[-1]) and tokens[-2] == '(':
        call()
    elif valid_id(tokens[-1]):
        tokens.pop()
        var_prime()
    elif is_num(tokens[-1]):
        tokens.pop()
    else:
        reject()


def call():
    watch_decent()
    if valid_id(tokens[-1]):
        tokens.pop()
        if tokens[-1] == '(':
            tokens.pop()
            args()
            if tokens[-1] == ')':
                tokens.pop()
            else:
                reject()
    else:
        reject()


def args():
    watch_decent()
    if tokens[-1] == '(' or is_num(tokens[-1]) or valid_id(tokens[-1]):
        arg_list()
    elif tokens[-1] == ')':
        return
    else:
        reject()


def arg_list():
    watch_decent()
    if valid_id(tokens[-1]):
        tokens.pop()
        arg_list_prime_prime_prime()
    elif tokens[-1] == '(':
        tokens.pop()
        expression()
        if tokens[-1] == ')':
            tokens.pop()
            term_prime()
            additive_expression_prime()
            simple_expression_prime()
            arg_list_prime()
        else:
            reject()
    elif is_num(tokens[-1]):
        tokens.pop()
        term_prime()
        additive_expression_prime()
        simple_expression_prime()
        arg_list_prime()
    else:
        reject()


def arg_list_prime():
    watch_decent()
    if tokens[-1] == ',':
        tokens.pop()
        expression()
        arg_list_prime()
    elif tokens[-1] == ')':
        return
    else:
        reject()


def arg_list_prime_prime():
    watch_decent()
    if tokens[-1] == '=':
        tokens.pop()
        expression()
        arg_list_prime()
    elif (is_rel_op(tokens[-1]) and tokens[-1] != '=') or is_math_op(tokens[-1]) or tokens[-1] == ',':
        term_prime()
        additive_expression_prime()
        simple_expression_prime()
        arg_list_prime()
    elif tokens[-1] == ')' or tokens[-1] == ',':
        term_prime()
        additive_expression_prime()
        simple_expression_prime()
        arg_list_prime()
    else:
        reject()


def arg_list_prime_prime_prime():
    watch_decent()
    if tokens[-1] == '(':
        tokens.pop()
        args()
        if tokens[-1] == ')':
            tokens.pop()
            term_prime()
            additive_expression_prime()
            simple_expression_prime()
            arg_list_prime()
        else:
            reject()
    elif tokens[-1] == '[':
        var_prime()
        arg_list_prime_prime()
    elif (is_rel_op(tokens[-1]) and tokens[-1] != '=') or is_math_op(tokens[-1]) or tokens[-1] == ',':
        arg_list_prime_prime()
    elif tokens[-1] == ')' or tokens[-1] == ',':
        var_prime()
        arg_list_prime_prime()
    else:
        reject()


watch_decent.counter = 0
tokens = []
j = 0
# Variables for tracking comments and nested comments
in_comment = False
comment_count = 0
# List to hold characters when dealing with spaceless inputs
char_list = []
with open(sys.argv[1], "r") as f:
    for line in f:
        # If the line is blank, skip it
        if line.isspace():
            continue
        else:
            # Print every line as we receive it. Strip white spaces off edges after printing
            # print("\nINPUT: " + line)
            line = line.strip()
        i = 0
        while i < len(line):
            # create variables for different characters in the line.
            char = line[i]
            prev_char = line[i - 1]
            next_index = i + 1
            next_next_index = i + 2
            end_of_line = len(line) - 1
            next_char = ""
            next_next_char = ""
            if next_index < len(line):
                next_char = line[i + 1]
            if next_next_index < len(line):
                next_next_char = line[i + 2]
            # this series of if statements deals with line comments and nested comments.
            if next_index < len(line) and char == '/':
                if next_char == '/':
                    break
                elif next_char == '*':
                    in_comment = True
                    if char_list:
                        compile_chlist(char_list)
                    comment_count += 1
                    if next_next_index < len(line):
                        if next_next_char == '/':
                            i += 2
                            continue
            if in_comment and next_index < len(line) and char == '*' and next_char == '/':
                comment_count -= 1
                i += 2
                continue
            if comment_count == 0:
                in_comment = False
            # If not in a comment, start creating tokens
            if not in_comment:
                # to deal with last character in a line. Needs to come first logically
                if i == end_of_line and not is_delimiter(char) and not is_math_op(char):
                    append_and_compile(char, char_list)
                # Since != is a unique token in it's the only use of !, the logic was a bit tricky.
                elif is_rel_op(char) or char == '!':
                    if char == '!' and next_char == '=':
                        if char_list:
                            compile_chlist(char_list)
                            char_list.append(char)
                            append_and_compile(next_char, char_list)
                            i += 2
                            continue
                        else:
                            char_list.append(char)
                            append_and_compile(next_char, char_list)
                            i += 2
                            continue
                    # this deals with 4<5
                    elif not is_rel_op(prev_char) and not is_rel_op(next_char):
                        if char_list:
                            compile_chlist(char_list)
                            append_and_compile(char, char_list)
                        else:
                            append_and_compile(char, char_list)
                    # this deals with 4<=5
                    elif not is_rel_op(prev_char) and is_rel_op(next_char):
                        compile_chlist(char_list)
                        char_list.append(char)
                    # this is how we handle === and how we also handle 4 <= 5 where there's delimiters between.
                    elif is_rel_op(prev_char) and len(char_list) == 1:
                        append_and_compile(char, char_list)
                    # this is the standard case when there is a delimiter.
                    elif not char_list:
                        if not is_rel_op(next_char):
                            append_and_compile(char, char_list)
                        else:
                            char_list.append(char)
                # Edge case to deal with exponents.
                elif is_math_op(char) and prev_char == 'E' and char_list[0].isdigit():
                    char_list.append(char)
                # if the character is a mathmatical operator or delimiter, then compile the list and check.
                elif is_delimiter(char) or is_math_op(char):
                    compile_chlist(char_list)
                    if char != ' ' and is_delimiter(char):
                        tokens.append(char)
                        # print char
                    elif is_math_op(char):
                        tokens.append(char)
                        # print "MATHOP:", char
                else:
                    char_list.append(char)

            i += 1

    if tokens:
        tokens.append("$")
        tokens.reverse()
        parser()
        '''tokens.reverse()
        print watch_decent.counter
        print tokens'''
        print "ACCEPT" if len(tokens) == 1 else "REJECT"
        
