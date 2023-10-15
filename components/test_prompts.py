from main import main
from prompt_builder import prompt
import time

def test():
    file_name = "hard"
    with open(f"{file_name}.txt", "r") as f:
        inputs = f.readlines()
        
    with open(f"{file_name}_output.txt", "w") as f:
        for inp in inputs:
            start = time.time()
            
            result = main(inp)
            running_time = round(time.time() - start)
            f.write("\n" + "-"*50 + "\n")
            f.write(f"INPUT: {inp}\n")
            f.write(f"------------- running_time={running_time}s ---------------\n")
            if result:
                f.write(str(result))
            else:
                f.write("No answer")
            
test()
