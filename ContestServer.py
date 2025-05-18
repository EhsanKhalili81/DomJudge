import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DomJudge.settings")  # Replace with your actual project name
django.setup()
import pika
import json
import binascii
import subprocess



import subprocess




def compiler(solution_file, input_file, expected_output_file,lang):
    try:
        with open(input_file, "r") as inp, open(expected_output_file, "r") as expected:
            input_lines = inp.readlines()
            expected_lines = expected.readlines()

        actual_output = []
        compile_structure = []
        if lang == 'python':
            compile_structure = ["python", solution_file]
        elif lang == 'java':
            compile_structure = ["java", solution_file]
        else:
            compile_structure = ["dotnet", "run" , "--no-build" ,solution_file]

        for line in input_lines:
            result = subprocess.run(
                compile_structure,
                input=line,
                capture_output=True,
                text=True,
                timeout=5 
            )
            actual_output.append(result.stdout.strip()) 

        correct = True
        for i in range(len(expected_lines)):
            expected_line = expected_lines[i].strip()
            actual_line = actual_output[i] if i < len(actual_output) else "Missing output"

            if expected_line != actual_line:
                correct = False
                print(f"❌ Test {i+1} failed!\nExpected: {expected_line}\nReceived: {actual_line}\n")
                print("False")
                return False

        if correct:
            print("True")
            return True

    except subprocess.TimeoutExpired:
        print("Time limit")
        return False
    except Exception as e:
        print(f"Error: {str(e)}")
        return False










from Judge.models import Submissions,Contester

def process_file(solution,input,output, metadata):
    if metadata['lang'] == 'python':
        solutionfile = "test.py"
    elif metadata['lang'] == 'java':
        solutionfile = "test.java"
    else:
        solutionfile = "test.cs"
    Inputs = "input.txt"
    Outputs = "output.txt"
    with open(solutionfile, "wb") as file:
        file.write(binascii.unhexlify(solution)) 

    with open(Inputs, "wb") as file:
        file.write(binascii.unhexlify(input)) 

    with open(Outputs, "wb") as file:
        file.write(binascii.unhexlify(output)) 
    result = compiler(solutionfile,Inputs,Outputs,metadata['lang'])
    contester = Contester.objects.get(id = metadata['contester_id'])
    question = contester.questions
    question[str(metadata['question_id'])]['tries'] += 1
    contester.questions = question
    # print("Contester ::::::::: ",contester)
    # submission = Submissions.objects.get(id = metadata['submission_id'])
    # submission.is_compiled = True
    if result:
        question[str(metadata['question_id'])]['result'] = True
        # print("tsetsstestestesessdfsfdsfdsfdsfdsfsd")
        contester.score += 10
    else:
        contester.penalty += 2
        # submission.score = submission.question.score
    contester.save()

    return True 
def callback(ch, method, properties, body):
    message = json.loads(body)
    metadata = message["metadata"]
    solution = message["solution"]
    input = message["input"]
    output = message["output"]


    success = process_file(solution,input,output ,metadata)

    if success:
        ch.basic_ack(delivery_tag=method.delivery_tag)

connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
channel = connection.channel()

channel.queue_declare(queue="file_queue")

channel.basic_consume(queue="file_queue", on_message_callback=callback, auto_ack=False) 

print("Compiling : ")
channel.start_consuming()
