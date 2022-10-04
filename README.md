Formal Language Practical Tasks

Programming languages used: Python 3.9
Test tools: pytest, pytest-cov

Tasks completed:
NFA to DFA, MinDFA

To convert NFA to DFA, CDFA, MinCDFA, use nfa2dfa.py:

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