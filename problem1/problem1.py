from typing import Set, Dict, Tuple, Optional
from collections import deque

class DFA:
    def __init__(self, states: Set[str], alphabet: Set[str], 
                 transitions: Dict[Tuple[str, str], str],
                 start_state: str, accept_states: Set[str]):

        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.accept_states = accept_states
    
    def get_next_state(self, current_state: str, symbol: str) -> Optional[str]:
        return self.transitions.get((current_state, symbol))

def are_dfas_equivalent(dfa1: DFA, dfa2: DFA) -> bool:
    if (dfa1.start_state in dfa1.accept_states) != (dfa2.start_state in dfa2.accept_states):
        return False
    queue = deque([(dfa1.start_state, dfa2.start_state)])
    visited = {(dfa1.start_state, dfa2.start_state)}
    while queue:
        state1, state2 = queue.popleft()
        for input_string in dfa1.alphabet.union(dfa2.alphabet):
            next_state1 = dfa1.get_next_state(state1, input_string)
            next_state2 = dfa2.get_next_state(state2, input_string)
            
            if next_state1 is None or next_state2 is None:
                continue
            
            if (next_state1 in dfa1.accept_states) != (next_state2 in dfa2.accept_states):
                return False
            
            if (next_state1, next_state2) not in visited:
                visited.add((next_state1, next_state2))
                queue.append((next_state1, next_state2))
    
    return True

if __name__ == "__main__":
    # Example 1: Two equivalent DFAs that accept strings with even number of 'a's
    dfa1 = DFA(
        states={'q0', 'q1'},
        alphabet={'a', 'b'},
        transitions={
            ('q0', 'a'): 'q1',
            ('q0', 'b'): 'q0',
            ('q1', 'a'): 'q0',
            ('q1', 'b'): 'q1'
        },
        start_state='q0',
        accept_states={'q0'}
    )
    
    dfa2 = DFA(
        states={'p0', 'p1'},
        alphabet={'a', 'b'},
        transitions={
            ('p0', 'a'): 'p1',
            ('p0', 'b'): 'p0',
            ('p1', 'a'): 'p0',
            ('p1', 'b'): 'p1'
        },
        start_state='p0',
        accept_states={'p0'}
    )
    
    print("Example 1 - Equivalent DFAs (2 states):")
    print(f"DFAs are equivalent: {are_dfas_equivalent(dfa1, dfa2)}")
    
    # Example 2: Two different DFAs with different initial state acceptance
    dfa3 = DFA(
        states={'q0', 'q1'},
        alphabet={'a', 'b'},
        transitions={
            ('q0', 'a'): 'q1',
            ('q0', 'b'): 'q0',
            ('q1', 'a'): 'q0',
            ('q1', 'b'): 'q1'
        },
        start_state='q0',
        accept_states={'q0', 'q1'}
    )
    
    dfa4 = DFA(
        states={'p0', 'p1'},
        alphabet={'a', 'b'},
        transitions={
            ('p0', 'a'): 'p1',
            ('p0', 'b'): 'p0',
            ('p1', 'a'): 'p0',
            ('p1', 'b'): 'p1'
        },
        start_state='p0',
        accept_states={'p1'}
    )
    
    print("\nExample 2 - Different DFAs (2 states, different initial state acceptance):")
    print(f"DFAs are equivalent: {are_dfas_equivalent(dfa3, dfa4)}")

    
    # Example 3: Two equivalent 3-state DFAs that accept strings ending with 'ab'
    dfa5 = DFA(
        states={'q0', 'q1', 'q2'},
        alphabet={'a', 'b'},
        transitions={
            ('q0', 'a'): 'q1',
            ('q0', 'b'): 'q0',
            ('q1', 'a'): 'q1',
            ('q1', 'b'): 'q2',
            ('q2', 'a'): 'q1',
            ('q2', 'b'): 'q0'
        },
        start_state='q0',
        accept_states={'q2'}
    )
    
    dfa6 = DFA(
        states={'p0', 'p1', 'p2'},
        alphabet={'a', 'b'},
        transitions={
            ('p0', 'a'): 'p1',
            ('p0', 'b'): 'p0',
            ('p1', 'a'): 'p1',
            ('p1', 'b'): 'p2',
            ('p2', 'a'): 'p1',
            ('p2', 'b'): 'p0'
        },
        start_state='p0',
        accept_states={'p2'}
    )
    
    print("\nExample 3 - Equivalent DFAs (3 states, accept strings ending with 'ab'):")
    print(f"DFAs are equivalent: {are_dfas_equivalent(dfa5, dfa6)}")
