This tool analyzes SPICE netlist files and simulation logs to detect circuit issues. It provides both rule-based and optional AI-powered suggestions using OpenAI’s GPT-3.5 model. Errors like unconnected nodes, incorrect BJT connections, and floating nodes are identified. It runs via command line with customizable file input and AI support.

To run the code follow

git clone https://github.com/Snehartha/esim_debugger
cd esim_debugger
pip install -r requirements.txt
 
Then run 
python netlist_parser.py --ai to get ai sugesstions.
