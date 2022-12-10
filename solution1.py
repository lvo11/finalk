
#--------------------------------------------------------------------------#
#                            List of KEYWORDS                             #
#--------------------------------------------------------------------------# 
KEYWORDS = [ 
	'and',
    'or',
    'not',
    'if',
    'elif',
    'else',
    'for',
    'while',
    'return',
    'continue',
    'break',
    'range',
    'in',
    'len'
]

BOOLEAN = [
    'True',
    'False'
]





#--------------------------------------------------------------------------#
#                            ERRORS                                        #
#--------------------------------------------------------------------------# 


# ERROR_TYPES = {
#         'IllegalCharError'      : 'Illegal Character',
#         'ExpectedCharError'     : 'Expected Character',
#         'InvalidSyntaxError'    : 'Expected Character',
#     }

# class error:
#     def __init__(self, err_name, info, pos):
#         self.err_name = err_name
#         self.info = info
#         self.pos = pos
    
#     def to_string(self):
#         result = f'{self.err_name}: {self.info}\n'
#         return result



TOKEN_CODE_DICT = {
    1: 'real_literal',
    2: 'natural_literal',
    3: 'bool_literal',
    4: 'char_literal',
    5: 'string_literal',
    6: 'keyworlds',
    7: 'special_symbols',
    8: 'variable/function identifier'
}

SPECIAL_SYMBOLS = ['+', '-', '*', '/', ':', '\n', '!', ',', '=', '<', '>', '(', ')']

#--------------------------------------------------------------------------#
#                            TOKENS                                        #
#--------------------------------------------------------------------------# 
class Token:
    def __init__(self, token_code, lexeme):
        self.lexeme = lexeme
        self.token_code = token_code

    def __repr__(self):
        a = TOKEN_CODE_DICT[self.token_code]
        return f'{a}:"{self.lexeme}"'



#--------------------------------------------------------------------------#
#                            LEXER                                         #
#--------------------------------------------------------------------------# 
class Lexer:
    def __init__(self, text):
        self.text = [*text]
        print(self.text)
        print(self.get_char_at(100))
        self.len_text = len(text)

    def generate_list_tokens(self):
        tokens = []
        i = 0
        while i < self.len_text:
            token = None
            c = self.get_char_at(i)
            if c == '#':
                i = self.skip_single_comment(i)
            elif c ==  '"' or c ==  "'":
                isBlockComment = self.is_block_comment(i)
                if isBlockComment:
                    i = self.skip_block_comment(i)
                else:
                    i, token = self.handle_string(i)
            elif c in SPECIAL_SYMBOLS:
                if c == '*':
                    i, token = self.handle_mul_or_exp(i)
                elif c == '/':
                    i, token = self.handle_div(i)
                elif c == '!':
                    i, token == handle_not_equal(i)
                    if token == None:
                        return None # error
                elif c == '=':
                    i, token = self.handle_equal_or_assign(i)
                elif c == '>' or c == '<':
                    i, token = self.handle_compare(i)
                else:
                    token = Token(7, c)
            

            # elif c ==  ':' or c == '\n':
            #     token = Token(c, 7)
            # elif c == '+':
            #     token = Token(c, 7)
            # elif c ==  '-':
            #     token = Token(c, 7)
            # elif c ==  '*':
            #     i, token = self.handle_mul_or_exp(i)
            # elif c == '%':
            #     token = Token(TOKEN_MOD)
            # elif c ==  '/':
            #     i, token = self.handle_div(i)
            # elif c ==  '(':
            #     token = Token(TOKEN_LPAREN)
            # elif c == ')':
            #     token = Token(TOKEN_RPAREN)
            # elif c == '!':
            #     i, token == handle_not_equal(i)
            #     if token == None:
            #         return None # error
            # elif c == '=':
            #     i, token = self.handle_equal_or_assign(i)
            # elif c == '<' or c == '>':
            #     i, token = self.handle_compare(i)
            # elif c == ',':
            #     token = Token(TOKEN_COMMA)
            elif c.isdigit():
                i, token = self.handle_number(i)
            elif c.isalpha():
                i, token = self.hanle_identifier(i)
                print(token)
            
            i = self.move_to_next_idx(i)
            if token is not None:
                tokens.append(token)
        
        print(tokens)
        return tokens
    
    def convert_list_chars_to_string(self, l):
        return "".join(l)
    

    def move_to_next_idx(self, i):
        return i + 1

    def move_idx_by(self, i, step):
        return i + step

    def is_valid_idx(self, i):
        return i >= 0 and i <= self.len_text

    def get_next_char(self, i):
        try:
            return self.text[i+1]
        except:
            return None

    def get_char_at(self, idx):
        try:
            return self.text[idx]
        except:
            return None

    def is_end(self, c):
        return (c == "") or (c == " ") or (c == "\n") or (c is None)

    def skip_single_comment(self, i):
        while self.is_valid_idx(i):
            if i != '\n':
                i = self.move_to_next_idx(i)
            else:
                return i

    def is_block_comment(self, i):
        try:
            next_char = self.get_next_char(i)
            next_next_char == self.get_char_at(i+2)
            return (next_char == '"' and next_next_char == '"') or (next_char == "'" and next_next_char == "'")
        except:
            return False

    def skip_block_comment(self, i):
        while self.is_valid_idx(i):
            if i != '"':
                i = self.move_to_next_idx(i)
            else:
                return self.move_idx_by(i, 2)

    def handle_string(self, i):
        i = self.move_to_next_idx(i)
        start_idx = i
        while self.is_valid_idx(i):
            c = self.get_char_at(i)
            print(c)
            if self.is_end(c):
                return i, None # cannot find close quote
            elif c == "'" or c == "\"":
                string = self.convert_list_chars_to_string(self.text[start_idx:i])
                return i, Token(5, string)
                i = self.move_to_next_idx(i)
            else:
                i = self.move_to_next_idx(i)
    
    def handle_mul_or_exp(self, i):
        next_char = self.get_next_char(i)
        if next_char == '*':
            return self.move_to_next_idx(i), Token(7, '**')
        else:
            return i, Token(7, '*')
    
    def handle_div(self, i):
        next_char = self.get_next_char(i)
        if next_char == '/':
            return self.move_to_next_idx(i), Token(7, '//')
        else:
            return i, Token(7, '/')
        

    def handle_not_equal(self, i):
        next_char = self.get_next_char(i)
        if next_char != "=":
            return i, None
        else:
            return self.move_to_next_idx(i), Token(7, '!=')

    def handle_equal_or_assign(self, i):
        next_char = self.get_next_char(i)
        if next_char == '=':
            return self.move_to_next_idx(i), Token(7, '==')
        else:
            return i, Token(7, '=')

    def handle_compare(self, i):
        is_less_compare = self.get_char_at(i) == '<'
        next_char = self.get_next_char(i)
        if next_char == '=':
            token = Token(7, '<=') if is_less_compare else Token(7, '>=')
            return self.move_to_next_idx(i), token
        else:
            token = Token(7, '<') if is_less_compare else Token(7, '>')
            return i, token

    def handle_number(self, i):
        start_idx = i
        i = self.move_to_next_idx(i)
        token = Token(2, '')
        number = ""
        while self.is_valid_idx(i):
            c = self.get_char_at(i)
            if self.is_end(c):
                number = self.convert_list_chars_to_string(self.text[start_idx :  i])
                token.lexeme = number
                return i, token
            elif c == ".":
                token = Token(1, '')
            elif c == "/":
                token = Token(1, '')
            elif not c.isdigit():
                return i, None
            i = self.move_to_next_idx(i)
            

    def hanle_identifier(self, i):
        identifier = ""
        token = None
        while self.is_valid_idx(i):
            c = self.get_char_at(i)
            if self.is_end(c):
                if token is None:
                    if identifier in KEYWORDS:
                        token = Token(6, identifier)
                    elif identifier in BOOLEAN:
                        token = Token(3, identifier)
                    elif identifier != "":
                        token = Token(8, identifier)
                    return i, token
                else:
                    token.lexeme = identifier
                    return i, token
            elif c == "_":
                token = Token(8, '')
            identifier += c
            i = self.move_to_next_idx(i)


class Parser:
    def __init__(self, token_list: list[Token]):
        self.token_list = token_list

    
    def build_tree(self):
        is_root = True
        for token in self.token_list:
            code = token.toke_code
            lexeme = token.lexeme
                
    
    def generate_experession(self):
        first_token_code = self.token_list[0].token_code
        if first_token_code == 6: #keyword
            keyword = self.token_list[0].lexeme
            if keyword == "if" or "elif" or "else":
                return "select statement"
            elif keyword == "for" or keyword == "while"
                return "for loop"
            return None
        if first_token_code == 8:
            next_token_code = self.token_list[1].token_code
            if next_token_code == 7 f
            

class Node:
    def __init__(self, is_root, expression=None, child=[]):
        self.expression = expression
        self.is_root = self.is_root
        self.child = child
    
    def add_child(self, child_node):
        self.child.append(child_node)


with open (r'sample.txt') as f:
    code = f.read()
    sample = Lexer(code)
    t_list = sample.generate_list_tokens()
    # print(code)
    # print(t_list)
    """
    Question 5:The selection statement is used to evaluate an expression 
    and run a certain code block based on the expression's outcome. 
    A mapping from a boolean expression to a list of instructions is the definition of the denotational semantics of the selection statement. 
    Depending on the outcome of the evaluation, 
    the expression is assessed and the set of instructions is carried out.
    Question 6: Loop Statement: The loop statement is utilized to repeatedly run a specific code block. 
    The mapping from a boolean expression to a list of instructions is the definition of the denotational semantics of the loop statement. 
    If the expression is true, the loop statement evaluates it and runs the code block's instructions. Until the expression returns false, 
    the loop statement will keep evaluating it and running the code block's instructions.
    Question 7: Expr Statement: A value is returned as a consequence of evaluating an expression using the expr statement. 
    A mapping from a collection of operations to a value is the definition of the denotational semantics of the expr statement. 
    A value is returned as a consequence of the operations' evaluation by the expr statement.
    Question 8 : Expr Statement (Boolean): The expr statement can be changed to yield a boolean answer (Expr Statement (Boolean)). 
    The mapping from a series of operations to a boolean value is the definition of the denotational semantics of the expr statement. 
    A boolean value is returned as a consequence of the expr statement's evaluation of the operations.
    Question 9 : 
    Attribute Grammar:

    Assignment Statement:

String + String -> Concatenate

String Natural -> Repeat

bool Natural -> Assign

Natural bool -> Assign

char Natural -> Assign

Natural char -> Assign

Natural Real -> Assign

No other types -> Error

Divide by zero -> Error

Modulo by zero -> Error
Question 10:
Syntactically Valid Assignment Statements:

Statement 1: a = 2 * (1 * b + a);

Semantic Rule Result: Pass


 

Statement 2: b=3*a-2

Semantic Rule Result: Pass


 

Statement 3: x = x + 2

Semantic Rule Result: Pass
Question 11:
Axiomatic Semantics:

A: a = 2* (b-1)-1 {a > 0}

Weakest Precondition: b > 0


 

B: if (x <y)

X = X +1

else

x = 3*X

{x < 0}

Weakest Precondition: x < 0 and y > 0


 

C: y=a* 2* (b-1)-1

if (x <y)

x = y + 1

else

x = 3* x

{x < 0}

Weakest Precondition: x < 0, y > 0, and a > 0, b > 0


 

D: a = 3 * (2 * b + a);

b=2*a-1

{b > 5}

Weakest Precondition: a > 0, b > 5
    """
    
     