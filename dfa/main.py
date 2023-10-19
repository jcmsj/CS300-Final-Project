import pytermgui as ptg
# M = (Q,Σ, δ, q0, F)
# Q = states
# Σ = input alphabet
# δ = transition function
# q0 = start state
# F - set of accepted states

def check(Q:set[str], sigma:set[str], delta:dict[str, dict[str,str|None]], start:str, F:set[str], input):
    state = start
    path: list[tuple[str, str] | str] = []
    for value in input:
        NEW_STATE = delta[state][value] or None

        if NEW_STATE != None:
            path.append((state, value))
            state = NEW_STATE
          
    path.append(state)
    return state in F, path

def main():
    # Starts with 1, any number of 0s in between, and ends with 1 over {0,1}
    # regex: 10*1
    input = "10001"
    F={"q3"}
    accepted, path = check(
        Q={"q0", "q1"},
        sigma={
            "0","1"
        },
        delta={
            "q0": {
                "1":"q1",
                "0": None
            },
            "q1": {
                "0": "q1",
                "1": "q3",
            },
            "q3": {
                "0": "q4",
                "1": "q4",
            }, 
            "q4": None,
        },
        start= "q0",
        F=F,
        input=input
    )

    print(f"Input: {input}")
    print(" -> ".join([f"{f'{p[0]}, {p[1]}' if type(p) == tuple else p}" for p in path]))
    print(f"Conclusion: {'Accepted' if accepted else 'Rejected'}")
    # with ptg.WindowManager() as wm:
    #     win = ptg.Window(
    #         ptg.Label(f"Input: {input}"),
    #         tuple(str(p) for p in path),
    #         ptg.Label(" -> ".join([str(p) for p in path])),
    #         ptg.Label(f"{accepted=}"),
    #         title="Deterministic Finite Automata"
    #     )
    #     wm.add(win)
    # print("Status: " + "accepted" if result else "rejected" ) # True

if __name__ == '__main__':
    main()
