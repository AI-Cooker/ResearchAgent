from main import main
import time

with open("example_inputs.txt", "r") as f:
    inputs = f.readlines()
    
with open("example_outputs1.txt", "w") as f:
    for inp in inputs:
        start = time.time()
        result = main(inp)
        running_time = round(time.time() - start)
        f.write("-"*50 + "\n")
        f.write(inp + "\n")
        f.write("-----\n")
        if result:
            f.write(result + "\n")
        else:
            f.write("No answer\n")