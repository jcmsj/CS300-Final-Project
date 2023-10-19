import random
import re

#  A Grammar describes a language's structure.
# G = (V, T, S, P)
# Where:
#   V = set of Nonterminal symbols
#   T = set of Terminal Symbols
#   S = Start symbol in V
#   P = set of Production rules
class RegularGrammar:
    def __init__(self, nonterminals:set[str], terminals:set[str], productions:dict[str, list[str]], start_symbol:str):
        self.nonterminals = nonterminals
        self.terminals = terminals
        self.productions = productions
        self.start_symbol = start_symbol
        self.re_non = re.compile("|".join(self.nonterminals))

    def generate(self):
        string = self.start_symbol
        done = False
        while not done:
            done = True
            for char in string:
                if char in self.productions:
                    substituted = random.choice(self.productions[char])
                    string = string.replace(char, substituted, 1)
                    done = False
                
        return string
    
    def test(self, input_str:str):
        if not self.valid_terminals(input_str):
            raise SyntaxError("input contains values not in the terminals")
        if not self.validate_productions():
            raise SyntaxError("Productions contain keys not in the nonterminals")

        # try to derive the 'input' from the self.productions
        d = self.start_symbol
        # S
        # S -> aSb
     
        while d != input_str:
            for i, char in enumerate(d):
                # Note: No need to check if char is a nonterminal.
                if char in self.productions:
                    d = self.replace_with_rule(d, self.productions[char], i, input_str)
                    if d == None:
                        return False
                    else:
                        break
                        # means that the rule is a terminal
            
        return True
    def replace(self, base:str, rule, i):
        _d = list(base)
        _d[i] = rule
        return "".join(_d)
    
    def replace_with_rule(self, base:str, rules:list[str], index:str, input_str:str):
        for rule in rules:
            if rule in self.terminals:
                d = self.replace(base, rule, index)
                # Done!
                if d == input_str:
                    return d
                continue

            d = self.replace(base, rule, index)

            # generated a string that is longer than the input string, which is wrong
            if len(d) > len(input_str):
                continue

            splitted = self.re_non.split(d, 2)
            [prefix, suffix] = splitted # assured to be ['' or an str, '' or an str]
            if (input_str.startswith(prefix) and input_str.endswith(suffix)):
                return d
            else:
                continue

        return None

    def validate_productions(self):
        # simply check if the two sets are equal
        return self.productions.keys() == self.nonterminals
    def valid_terminals(self, input:str):
        for char in input:
            if char not in self.terminals:
                return False
            
        return True

# grammar = RegularGrammar(
    # nonterminals={
        # "S"
    # },
    # terminals={
        # "a", 
        # "b", 
    # },
    # productions={
        # "S": ["aSb", "b", "bA"],
        # "A": ["cS"]
    # },
    # start_symbol="S",
# )

# Generate a string from the grammar.
# string = grammar.generate()

# String that ends with b over {a,b}
# ab abb abbb
grammar = RegularGrammar(
    nonterminals={
        "S"
    },
    terminals={
        "a", 
        "b", 
    },
    productions={
        "S": ["aSb", "b"],
    },
    start_symbol="S",
)
#  T, T, F, T, F
print([grammar.test(s) for s in ['b', 'abb', 'ab', 'aabbb', 'ba']])

endswithD = RegularGrammar(
    nonterminals={
        "S"
    },
    terminals={
        "a", 
        "b",
        "c",
        "d" 
    },
    productions={
        "S": ["aS", "bS", "cS", "dS","d"],
    },
    start_symbol="S",
)

print(endswithD.test("accd"))
print([endswithD.generate() for i in range(100)])
