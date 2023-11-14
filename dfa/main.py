import json
from sys import argv

# M = (Q,Σ, δ, q0, F)
# Q = states
# Σ = input alphabet
# δ = transition function
# q0 = start state
# F - set of accepted states
def check(Q:set[str], sigma:set[str], delta:dict[str, dict[str,str|None]], start:str, F:set[str], input_str):
    """Returns a tuple of whether the input is accepted and the path taken"""

    # check that all states are in the transition function
    q_complement = Q - delta.keys()
    if len(q_complement) > 0:
        raise Exception(f"States {q_complement} are unused in the the transition function")
    # and that all states in the transition function are in the set of states
    delta_complement = delta.keys() - Q
    if len(delta_complement) > 0:
        raise Exception(f"{delta_complement} found in the Transition function are NOT specified in Q")
    
    # check that all the input characters are in the alphabet
    input_set = set([c for c in input_str])
    input_complement = input_set - sigma
    if len(input_complement) > 0:
        raise Exception(f"The characters {input_complement} from the input string are not in the alphabet {sigma}")
    
    # check delta for transitions that are not in the alphabet
    for state in delta:
        transitions = delta[state]
        if transitions != None:
            for value in transitions:
                if value not in sigma:
                    raise Exception(f"{value} is not in the alphabet {sigma}, but is used in the transitions of {state}. Please remove this transition or add it to the alphabet")

    state = start
    path: list[tuple[str, str] | str] = []
    # Iterate through the input
    for value in input_str:
        if delta[state] == None:
            """ Allow elliding the transitions for an entire state"""
            continue
        # Find the next state given the current state and the current character from the input
        NEW_STATE = delta[state].get(value)

        if NEW_STATE != None:
            path.append((state, value))
            state = NEW_STATE
          
    path.append(state)
    return state in F, path

def pretty_path(path:list[tuple[str, str] | str]):
    """Pretty print the path taken by the DFA
    Example output:\n q0, 1 -> q1, 1 -> q2"""
    return " -> ".join([f"{f'{p[0]}, {p[1]}' if type(p) == tuple else p}" for p in path])

def read_json_file(filepath: str) -> dict:
    with open(filepath, 'r') as f:
        data = json.load(f, )
    return data

def main():
    '''Run if main module'''
    """Note: the included sample.json is a DFA that accepts binary strings that starts and ends with 1 having zero or more 0s in between"""
    "or simply in REGEX:: 10*1"
    match argv:
        case [_, "-dfa", dfa_filepath, "-i", input_str]:
            DFA = read_json_file(dfa_filepath)
            print("DFA:")
            # Pretty print the dfa
            print(json.dumps(DFA, indent=2))

            status, path = check(
                Q=set(DFA["states"]),
                sigma=set(DFA["alphabet"]),
                delta=DFA["transition_function"],
                start=DFA["start_state"],
                F=set(DFA["accept_states"]),
                input_str=input_str
            )
            print(f"Input:\n{input_str}")
            print("Path:")
            print(pretty_path(path))
            if status:
                print("Conclusion: Accepted")
            else:
                print(f"Conclusion: Rejected")
           
        case _:
            print("Usage: python -dfa <dfa_filepath> -i <input_str>")

if __name__ == '__main__':
    main()
