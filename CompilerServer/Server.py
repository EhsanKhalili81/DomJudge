import pika
import json
import binascii
import subprocess
# import pika

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
                return False

        if correct:
            print("✅ All test cases passed!")
            return True

    except subprocess.TimeoutExpired:
        print("⏳ Time limit exceeded!")
        return False
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

# Example usage
# solution_file = "1.py"
# input_file = "input.txt"
# expected_output_file = "output.txt"

# compile_and_check(solution_file, input_file, expected_output_file)


# from Judge.utils import pythonCompiler
from Judge.models import Submissions
def process_file(solution,input,output, metadata):
    pythonFIle = "test.py"
    Inputs = "input.txt"
    Outputs = "output.txt"
    with open(pythonFIle, "wb") as file:
        file.write(binascii.unhexlify(solution))  # Convert back from hex

    with open(Inputs, "wb") as file:
        file.write(binascii.unhexlify(input)) 

    with open(Outputs, "wb") as file:
        file.write(binascii.unhexlify(output)) 
    result = pythonCompiler(pythonFIle,Inputs,Outputs)
    submission = Submissions.objects.get(id = metadata['submission_id'])
    submission.is_compiled = True
    if result:
        submission.final_result = True
        submission.score = submission.question.score
    submission.save()
    return True  # Indicating successful processing

def callback(ch, method, properties, body):
    message = json.loads(body)
    metadata = message["metadata"]
    solution = message["solution"]
    input = message["input"]
    output = message["output"]


    success = process_file(solution,input,output ,metadata)

    if success:
        ch.basic_ack(delivery_tag=method.delivery_tag)  # ✅ Remove message from queue after processing
        print(f" [✓] Message deleted after processing for {metadata['user_id']}")

connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
channel = connection.channel()

channel.queue_declare(queue="file_queue")

channel.basic_consume(queue="file_queue", on_message_callback=callback, auto_ack=False)  # Ensure manual deletion

print(" [*] Waiting for files...")
channel.start_consuming()
