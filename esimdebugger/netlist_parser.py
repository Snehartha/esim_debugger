import os
import openai
from collections import defaultdict
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY") # open api key in .env file



# rule based suggestions
def get_rule_based_suggestion(issue, context):
    suggestions = {
        'unconnected_node': f"Node {context} is only connected to one component. Consider connecting it to another node or ground.",
        'missing_connection': f"Component '{context}' has fewer than 2 connected nodes. Check for typos or incomplete definitions.",
        'bjt_misconnection': f"BJT '{context}' should have 3 nodes (Collector, Base, Emitter). Check the netlist syntax."
    }
    return suggestions.get(issue, "No suggestion available.")




# ai suggestions with gpt-3.5-turbo model
def get_ai_suggestion(issue):
    #try the code
    try:
        response = openai.chat.completions.create(
          model="gpt-3.5-turbo",
          messages=[
             {"role": "system", "content": "You are a helpful assistant."},
             {"role": "user", "content":issue},
          ]
        )
        reply = response.choices[0].message.content
        return response['choices'][0]['message']['content'].strip()
    #if not then throw the error
    except Exception as e:
        return f"(AI Error) {str(e)}"



    #parsing the list
def parse_netlist(file_path):
    components = []
    node_usage = defaultdict(int)

    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith(('*', '.', '+')):
                continue

            tokens = line.split()
            name = tokens[0].upper()
            comp_type = name[0]

            # Basic component nodes
            if comp_type in ['R', 'C', 'L', 'V', 'I']:
                nodes = tokens[1:3]
            elif comp_type == 'Q':  # BJT
                nodes = tokens[1:4]
            else:
                nodes = tokens[1:3]

            components.append({
                'name': name,
                'type': comp_type,
                'nodes': nodes,
                'line': line
            })

            for node in nodes:
                if node != '0':
                    node_usage[node] += 1

    return components, node_usage



#checking the netlist
def check_netlist(components, node_usage, use_ai=False):
    print("[✓] Netlist Loaded\n")

    for comp in components:
        if len(comp['nodes']) < 2:
            issue = f"Component {comp['name']} has fewer than 2 connections." #for missing connections
            print(f"[!] Error: {issue}")
            print("Rule-Based Suggestion:", get_rule_based_suggestion('missing_connection', comp['name']))
            if use_ai:
                print("AI Suggestion:", get_ai_suggestion(issue))

        if comp['type'] == 'Q' and len(comp['nodes']) != 3:  #BJT
            issue = f"BJT {comp['name']} has incorrect number of pins (found {len(comp['nodes'])})."
            print(f"[!] Warning: {issue}")
            print("    Rule-Based Suggestion:", get_rule_based_suggestion('bjt_misconnection', comp['name']))
            if use_ai:
                print("AI Suggestion:", get_ai_suggestion(issue))

    for node, count in node_usage.items():
        if count == 1:
            issue = f"Node {node} is only used once."   #for unconnected nodes
            print(f"[!] Warning: {issue}")
            print("Rule-Based Suggestion:", get_rule_based_suggestion('unconnected_node', node))
            if use_ai:
                print("AI Suggestion:", get_ai_suggestion(issue))



def main():
    import argparse   #to make it the tool
    parser = argparse.ArgumentParser()
    parser.add_argument("--ai", action="store_true", help="Enable AI-powered suggestions")
    parser.add_argument("--file", type=str, default=r"C:\Users\sneha\esimdebugger\sampledata\bjt_amplifier.cir.out", help="Path to netlist file")
    # change the default into the path of the file(.cir||.cir.out)
    args = parser.parse_args()

    components, node_usage = parse_netlist(args.file)
    check_netlist(components, node_usage, use_ai=args.ai)

if __name__ == "__main__":
    main()
