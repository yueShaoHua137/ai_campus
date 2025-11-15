"""
Alias to run the knowledge_builder script (keeps naming consistent with README).
"""
import subprocess
import sys

if __name__ == '__main__':
    # call existing knowledge_builder.py
    subprocess.check_call([sys.executable, 'knowledge_builder.py'])
