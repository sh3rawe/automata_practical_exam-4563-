def is_prime(n):
    """Checks if a number is prime."""
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

class TuringMachineSimulator:
    def __init__(self, input_string, blank_symbol='B', marked_symbol='X'):
        self.tape = list(input_string)
        self.tape.extend([blank_symbol] * (max(10, len(input_string) + 10)))
        self.head = 0
        self.state = 'start'
        self.blank_symbol = blank_symbol
        self.marked_symbol = marked_symbol
        self.count = 0

    def transition(self):
        if self.state in {'accept', 'reject'}:
            return False

        current_symbol = self.tape[self.head]

        if self.state == 'start':
            if current_symbol == '1':
                self.tape[self.head] = self.marked_symbol
                self.count += 1
                self.head += 1
                self.state = 'marking'
            elif current_symbol == self.blank_symbol:
                self.state = 'check_prime'
            elif current_symbol == self.marked_symbol:
                self.state = 'reject'
            else:
                self.state = 'reject'
        
        elif self.state == 'marking':
            if current_symbol == '1':
                self.tape[self.head] = self.marked_symbol
                self.count += 1
                self.head += 1
            elif current_symbol == self.blank_symbol or current_symbol == self.marked_symbol:
                self.state = 'check_prime'
            else:
                self.state = 'reject'

        elif self.state == 'check_prime':
            if is_prime(self.count):
                self.state = 'accept'
            else:
                self.state = 'reject'

        return True

    def run(self, base_max_steps=50):
        steps = 0
        max_steps = (len(self.tape) - list(self.tape).count(self.blank_symbol)) + base_max_steps
        initial_tape_str = "".join(self.tape).rstrip(self.blank_symbol)
        if not initial_tape_str and len(self.tape) > 0 and self.tape[0] == self.blank_symbol:
             initial_tape_str = "(empty)"

        print(f"Initial: Input='{initial_tape_str}', State: {self.state}, Head: {self.head}, Count: {self.count}")
        self._print_tape_config(steps)

        while self.state not in {'accept', 'reject'} and steps < max_steps:
            step_taken = self.transition()
            if not step_taken:
                break 
            steps += 1
            self._print_tape_config(steps)

        if steps >= max_steps and self.state not in {'accept', 'reject'}:
            print("TM reached max_steps without halting.")
            return "Reject (Max Steps)"

        final_result = "Accept" if self.state == 'accept' else "Reject"
        print(f"Halted. Final State: {self.state}. Result: {final_result}")
        return final_result

    def _print_tape_config(self, step_num_or_label):
        tape_display = ''.join(self.tape)
        head_marker = [' '] * len(tape_display)
        if 0 <= self.head < len(head_marker):
             head_marker[self.head] = '^'
        
        display_limit = 70
        tape_segment = tape_display
        head_marker_segment = "".join(head_marker)

        if len(tape_display) > display_limit:
            start_idx = max(0, self.head - display_limit // 2)
            end_idx = min(len(tape_display), start_idx + display_limit)
            if end_idx - start_idx < display_limit and start_idx > 0:
                start_idx = max(0, end_idx - display_limit)
            
            tape_segment = tape_display[start_idx:end_idx]
            head_marker_segment = "".join(head_marker[start_idx:end_idx])
            
            if start_idx > 0:
                tape_segment = "..." + tape_segment
                head_marker_segment = "   " + head_marker_segment
            if end_idx < len(tape_display):
                tape_segment = tape_segment + "..."
        
        step_label = f"Step {step_num_or_label:<3}" if isinstance(step_num_or_label, int) else str(step_num_or_label)

        print(f"{step_label}: State: {self.state:<12}, Head: {self.head:2}, Count: {self.count:2}")
        print(f"        Tape: {tape_segment}")
        print(f"              {head_marker_segment}")

def turing_machine_prime_unary_simulated(unary_string_input):
    if not all(char == '1' for char in unary_string_input):
        print(f"Input: '{unary_string_input}'")
        print("Error: Input string must be unary (contain only '1's). Not in language.")
        return "Reject"
    tm = TuringMachineSimulator(input_string=unary_string_input)
    return tm.run()

if __name__ == "__main__":
    test_cases = {
        "": 0,
        "1": 1,
        "11": 2,
        "111": 3,
        "1111": 4,
        "11111": 5,
        "111111": 6,
        "1111111": 7,
        "11111111111": 11,
        "1" * 13: 13,
        "1" * 15: 15,
    }

    for s, length_val in test_cases.items():
        print(f"\n--- Testing input: '{s}' (Length: {length_val}) ---")
        result = turing_machine_prime_unary_simulated(s)
        
        expected_prime_check = is_prime(length_val)
        expected_outcome = "Accept" if expected_prime_check else "Reject"
        
        print(f"Input: '{s}' (len {length_val}), Primality: {expected_prime_check}, TM Output: {result}, Expected: {expected_outcome}")
        
        correct_rejection = (expected_outcome == "Reject" and result.startswith("Reject"))
        correct_acceptance = (expected_outcome == "Accept" and result == "Accept")

        if correct_rejection or correct_acceptance:
            print("Test Passed.")
        else:
            print(f"Test FAILED. Got {result}, Expected {expected_outcome}")

    print("\n--- Testing non-unary input: '101' ---")
    result_non_unary = turing_machine_prime_unary_simulated("101")
    print(f"Input: '101', TM Output: {result_non_unary}, Expected: Reject")
    if result_non_unary == "Reject":
        print("Test Passed (non-unary correctly rejected).")
    else:
        print("Test FAILED (non-unary not rejected as expected).")
