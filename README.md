# Formal Language Practical Tasks

Programming languages used: Python 3.9  
Test tools: pytest, pytest-cov

Tasks completed:  
NFA to DFA, MinDFA

To convert NFA to DFA, CDFA, MinCDFA, use `nfa2dfa.py`:

usage: `nfa2dfa.py [-h] [--alphabet ALPHABET] --nfa_doa NFA_DOA [-cdfa] [-mincdfa] [--dfa_doa DFA_DOA] [-graph] [--graph_name GRAPH_NAME]`

options: <br/>
  -h, --help.........................................show this help message and exit <br/>
  --alphabet..........ALPHABET...........Alphabet <br/>
  --nfa_doa............NFA_DOA...........NFA .doa file <br/>
  -cdfa...............................................To make CDFA <br/>
  -mincdfa.........................................To make MinCDFA <br/>
  --dfa_doa...........DFA_DOA............Name of .doa output file <br/>
  -graph.............................................To make graphviz <br/>
  --graph_name....GRAPH_NAME....Name of graphviz output file, requires -graph. <br/> 
  ........................................................By default writes in terminal 

Example (write command in the root of project):   
`python3 nfa2dfa.py --nfa_doa my_nfa.doa -mincdfa -dfa_doa my_mincdfa.doa --graph`  
It will make a my_mincdfa.doa file with description of MinCDFA isomorphic to NFA from my_nfa.doa. Also it will translate .doa format to graphviz and write it in a terminal

To convert regex to machine, use `regex2machine.py`:

usage: `regex2machine.py [-h] --regex REGEX [--alphabet ALPHABET] [-dfa] [-cdfa] [-mincdfa] [-study_mode STUDY_MODE] [-doa] [--doa_name DOA_NAME] [-graph] [--graph_name GRAPH_NAME]`

options:  
  -h, --help.........................................show this help message and exit  
  --regex...............REGEX................Your regex in reverse polish notation  
  --alphabet..........ALPHABET..........Alphabet  
  -dfa................................................To make DFA  
  -cdfa..............................................To make CDFA  
  -mincdfa.........................................To make MinCDFA  
  -study_mode.....STUDY_MODE....Will made .doa files for each steps  
  -doa................................................To make .doa output file  
  --doa_name......DOA_NAME..........Name of .doa file, requires -doa  
  -graph.............................................Convert to graphviz  
  --graph_name....GRAPH_NAME....Name of graphviz output file, requires -graph.  
........................................................By default writes in terminal  

Example (write command in root of project):  
`python3 regex2machine.py --alphabet="abc" --regex="ab ^* c + ab EPS + *" -cdfa -doa --doa_name="my_doa.doa"`  
It will make a NFA fron regex ((ab)* + c)(ab + ε), then build CDFA and write it's descriptions in my_doa.doa


### To run test:
(write commands in root of project)  
`pytest --cov=sources.Machines -vv` (classical way)  
`coverage run --source=sources.Machines -m pytest -vv test_by_pytest && coverage report -m`
(this command shows missing lines)

### Structure:
`sources.Machines`: `NFA.py, DFA.py and MinCDFA.py`  
`sources.parse_and_translate`: parsing (regex <-> nfa), translation (.doa <-> machine)  
`test_by_pytest`: pytests and .doa files for tests  
`borrowing`: Mikhail's code of translation (with my modifications)