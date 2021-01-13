import subprocess
import sys

def execution(input_filename):
    # CADの操作と体積の計算
    command1 = subprocess.run(['python3', 'extcode_1.py', input_filename])
    # シミュレーションの実行
    command2 = subprocess.run(['python3', 'extcode_2.py'])


if __name__ == "__main__":
    input_filename = sys.argv[1]

    execution(input_filename)
