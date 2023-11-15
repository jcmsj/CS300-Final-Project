import json
import random
import re
from sys import argv
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
        """ Returns a tuple of whether the input is accepted and the path taken"""
        self.validate_terminals(input_str)
        d = self.start_symbol
        path: list[str] = [d]
        # try to derive the 'input' from the self.productions
        while d != input_str:
            for i, char in enumerate(d):
                if char in self.productions:
                    d = self.try_rules(d, self.productions[char], i, input_str)
                    path.append(str(d))
                    if d == None:
                        return False, path
                    else:
                        break
                        # means that the rule is a terminal
            
        return True, path
    
    # Replaces the char at i with the rule
    def replace(self, base:str, rule:str, i:int):
        _d = list(base)
        _d[i] = rule
        return "".join(_d)
    
    def try_rules(self, base:str, rules:list[str], index:int, input_str:str):
        """Tries every rule until it finds one that matches the input_str or its prefix and suffix.\n
        Returns the rule and the new string if it matches the input_str,\n otherwise returns None"""
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
            raise Exception(f"{unused_nonterminals} are never used in the production rules. Please remove these")
        
    def validate_terminals(self, input_str:str):
        for char in input_str:
            if char not in self.terminals:
                raise Exception(f"{char} is not a member of the terminals {self.terminals}")
        # TODO: check if the terminals are used in the production rules
        # TODO: check if there are terminals in the production rules that are not listed in the self.terminals

        return True

def read_json_file(filepath: str) -> dict:
    with open(filepath, 'r') as f:
        data = json.load(f, )
    return data

def run_sample(g: RegularGrammar, count:int):
    print(f"{count} unique sample strings:")
    unique: set[str] = set()

    while len(unique) < count:
        unique.add(g.generate())
    for i, string in enumerate(unique):
        print(f"{i+1}) {string}")

def cli():
    import argparse
    parser = argparse.ArgumentParser(description='A program that can validate and generate strings from a Regular Grammar')
    parser.add_argument('-g', '--grammar', type=str, help='filepath to the Regular Grammar json file')
    parser.add_argument('-i', '--input', type=str, help='input string to validate')
    parser.add_argument('-s', '--sample', type=int, help='number of sample strings to generate')
    return parser.parse_args(), parser
def main():
    #  Match argv for a -g flag with a filepath and -i flag with an input string
    args, argparser = cli()
    if args.grammar != None:
        if args.input:
            # Read the json file
            raw_grammar = read_json_file(args.grammar)
            # Pretty print the json
            print(json.dumps(raw_grammar, indent=2))
            # Check if the input string is accepted by the grammar
            grammar = RegularGrammar(**raw_grammar)
            accepted, path = grammar.test(args.input)
            print(f"Input:\n{args.input}")
            print("Path:")
            print(" -> ".join(path))
            print(f"Conclusion: {'Accepted' if accepted  else 'Rejected'}")
            return
        elif args.sample:
            run_sample(
                RegularGrammar(**read_json_file(args.grammar)), 
                args.sample
            )
            return
        
    argparser.print_help()
if __name__ == '__main__':
    main()
