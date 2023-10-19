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
        self.nonterminals_regex = re.compile("|".join(self.nonterminals))
        self.validate_productions()
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
  
        self.validate_terminals(input_str)
        d = self.start_symbol
        # try to derive the 'input' from the self.productions
        while d != input_str:
            for i, char in enumerate(d):
                if char in self.productions:
                    d = self.try_rules(d, self.productions[char], i, input_str)
                    if d == None:
                        return False
                    else:
                        break
                        # means that the rule is a terminal
            
        return True
    
    # Replaces the char at i with the rule
    def replace(self, base:str, rule:str, i:int):
        _d = list(base)
        _d[i] = rule
        return "".join(_d)
    
    def try_rules(self, base:str, rules:list[str], index:str, input_str:str):
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

            # assured to be ['' or an str, '' or an str]
            [prefix, suffix]= self.nonterminals_regex.split(d, 2)

            # If the prefix/suffix of the new string matches that of the input, then we're in the right track
            if (input_str.startswith(prefix) and input_str.endswith(suffix)):
                return d
            else: # try next rule
                continue

        return None

    def validate_productions(self):
        # simply check if the two sets are equal
        if self.productions.keys() == self.nonterminals:
            return True
        extra_production = self.productions.keys() - self.nonterminals
        if len(extra_production) > 0:
            raise Exception(f"{extra_production} are not members of the nonterminals {self.nonterminals}")
        
        unused_nonterminals = self.nonterminals - self.productions.keys()
        if len(unused_nonterminals) > 0:
            raise Exception(f"{unused_nonterminals} are never used in the production rules")
        
    def validate_terminals(self, input_str:str):
        for char in input_str:
            if char not in self.terminals:
                raise Exception(f"{char} is not a member of the terminals {self.terminals}")
        # TODO: check if the terminals are used in the production rules
        # TODO: check if there are terminals in the production rules that are not listed in the self.terminals

        return True

def main():
    '''Run if main module'''
    # grammar = RegularGrammar(
#     nonterminals={
#         "S",
#         "A"
#     },
#     terminals={
#         "a", 
#         "b",
#         "c",
#     },
#     productions={
#         "S": ["aSb", "b", "bA"],
#         "A": ["cS"]
#     },
#     start_symbol="S"
# )
    # String that ends with b over {a,b}
    # Description: a's followed by b's that is one more than a, there can be 0 number of a's
    # examples: ab abb abbb
    letter_as_followed_by_letter_bs = RegularGrammar(
        nonterminals={
            "S",
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

    example = input("Choose example: \n[0] grammar that ends with d over {a,b,c,d}\n[1] a's followed by b's that is one more than a, there can be 0 number of a's \n> ")
    grammar = endswithD if example == '0'  else letter_as_followed_by_letter_bs
    if example == '0':
        # T T F F T
        print({s:grammar.test(s) for s in ['d', 'abd', 'ab', 'aabbb', 'bad']})
    elif example == '1':
        #  T T F T F
        print({s:grammar.test(s) for s in ['b', 'abb', 'ab', 'aabbb', 'ba']})

    for sample in [grammar.generate() for _ in range(100)]:
        print(sample)

if __name__ == '__main__':
    main()

