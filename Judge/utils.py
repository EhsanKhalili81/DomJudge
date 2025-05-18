import pika
import json

def send_file(solution,input,output, metadata):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
    channel = connection.channel()
    
    channel.queue_declare(queue="file_queue")

    with open(solution, "rb") as file:
        file_data = file.read()
    with open(input, "rb") as file:
        file_data2 = file.read()

    with open(output, "rb") as file:
        file_data3 = file.read()
    message = {
        "metadata": metadata,
        "solution": file_data.hex() ,
         "input": file_data2.hex(),
         "output": file_data3.hex() 
    }

    channel.basic_publish(exchange="", routing_key="file_queue", body=json.dumps(message))
    print("File is Sent")

    connection.close()



def contest_send_file(solution,input,output, metadata):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
    channel = connection.channel()
    
    channel.queue_declare(queue="file_queue")

    with open(solution, "rb") as file:
        file_data = file.read()
    with open(input, "rb") as file:
        file_data2 = file.read()

    with open(output, "rb") as file:
        file_data3 = file.read()
    message = {
        "metadata": metadata,
        "solution": file_data.hex() ,
         "input": file_data2.hex(),
         "output": file_data3.hex() 
    }

    channel.basic_publish(exchange="", routing_key="file_queue", body=json.dumps(message))
    print("File is Sent")

    connection.close()

