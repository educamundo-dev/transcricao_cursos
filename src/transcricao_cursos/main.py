import gc
import sys 
#!/usr/bin/env python
from transcricao_cursos.crew import TranscricaoCursosCrew

input_cmd = sys.argv[1]

gc.collect()

def run():
    # Replace with your inputs, it will automatically interpolate any tasks and agents information
    inputs = {
        'topic': input_cmd
    } 
    TranscricaoCursosCrew().crew().kickoff(inputs=inputs)

