import subprocess

def main():
    for i in range(1, 6):
        filename = f"testes/teste{i}.txt"
        
        # Execute the command and capture the output
        subprocess.run(['python3', 'main.py', filename])
        with open('output.txt', 'r') as file:
            output = file.read().strip()

        expected_output_file = f"testes/output{i}.txt"
        with open(expected_output_file, 'r') as f:
            expected_output = f.read().strip()

        if output == expected_output:
            print(f"Test {i} ✔ : Output gerad0 está correto.")
        else:
            print(f"Test {i} X : Output gerado está errado.")

if __name__ == "__main__":
    main()
