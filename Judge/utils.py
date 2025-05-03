import subprocess

def pythonCompiler(solution_file, input_file, expected_output_file):
    try:
        # Read input file line by line
        with open(input_file, "r") as inp, open(expected_output_file, "r") as expected:
            input_lines = inp.readlines()
            expected_lines = expected.readlines()

        actual_output = []
        
        # Run solution.py for each line of input
        for line in input_lines:
            result = subprocess.run(
                ["python", solution_file],
                input=line,
                capture_output=True,
                text=True,
                timeout=5  # Set time limit
            )
            actual_output.append(result.stdout.strip())  # Collect actual output

        # Compare line by line
        correct = True
        for i in range(len(expected_lines)):
            expected_line = expected_lines[i].strip()
            actual_line = actual_output[i] if i < len(actual_output) else "Missing output"

            if expected_line != actual_line:
                correct = False
                print(f"❌ Test {i+1} failed!\nExpected: {expected_line}\nReceived: {actual_line}\n")

        if correct:
            print("✅ All test cases passed!")

    except subprocess.TimeoutExpired:
        print("⏳ Time limit exceeded!")
    except Exception as e:
        print(f"Error: {str(e)}")

# Example usage
# solution_file = "1.py"
# input_file = "input.txt"
# expected_output_file = "output.txt"

# compile_and_check(solution_file, input_file, expected_output_file)

