import datetime
import numpy as np
import tkinter as tk
from tkinter import messagebox
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

canvas_ref = None

class Graph:
    def __init__(self, vertices, edges):
        self.vertices = set(vertices)
        self.edges = set(frozenset(edge) for edge in edges)

    def __add__(self, other):
        vertices = self.vertices.union(other.vertices)
        edges = self.edges.union(other.edges)
        return Graph(vertices, edges)

    def __mul__(self, other):
        vertices = self.vertices.union(other.vertices)
        edges = self.edges.union(other.edges)
        new_edges = set(frozenset([u, v]) for u in self.vertices for v in other.vertices if u != v)
        return Graph(vertices, edges.union(new_edges))

    def induce(self, nodes):
        """Generate an induced subgraph over the given nodes."""
        nodes = set(nodes)
        induced_edges = set(edge for edge in self.edges if edge.issubset(nodes))
        return Graph(nodes, induced_edges)

def v(node_name):
    return Graph({node_name}, set())

# ... [Parsing functions] ...

def tokenize(expression):
    tokens = []
    current_token = ""
    for char in expression:
        if char.isspace():
            continue
        if char in ("*", "+", "(", ")"):
            if current_token:
                tokens.append(current_token)
                current_token = ""
            tokens.append(char)
        else:
            current_token += char
    if current_token:
        tokens.append(current_token)
    return tokens

def parse_graph(expression):
    tokens = tokenize(expression)
    graph = parse_expression(tokens)
    return graph

# ... [The rest of the parsing functions remain the same, but we modify parse_factor] ...
def parse_expression(tokens):
    graph = parse_term(tokens)
    while tokens and tokens[0] == "+":
        tokens.pop(0)
        graph += parse_term(tokens)
    return graph

def parse_term(tokens):
    graph = parse_factor(tokens)
    while tokens and tokens[0] == "*":
        tokens.pop(0)
        graph *= parse_factor(tokens)
    return graph


def parse_factor(tokens):
    if tokens[0] == "(":
        tokens.pop(0)
        graph = parse_expression(tokens)
        if tokens[0] != ")":
            raise ValueError("Invalid expression: missing closing parenthesis")
        tokens.pop(0)
        return graph
    else:
        vertex = tokens.pop(0)
        return v(vertex)
    


def save_graph_to_file(graph_name, expression):
    with open(f"{graph_name}.txt", "w") as file:
        file.write(expression)

def load_graph_from_file(graph_name):
    try:
        with open(f"{graph_name}.txt", "r") as file:
            graph_expression = file.read().strip()
        return parse_graph(graph_expression)
    except FileNotFoundError:
        return None

def visualize_graph(g):

    global canvas_ref  # Declare the global variable

    # If there's an existing canvas, destroy it
    if canvas_ref:
        canvas_ref.get_tk_widget().destroy()

    # Convert the Graph object to a networkx Graph
    nx_graph = nx.Graph()
    nx_graph.add_nodes_from(g.vertices)
    nx_graph.add_edges_from(g.edges)
    
    # Create a new figure
    fig = plt.figure()

    # Compute circular layout positions
    n = len(g.vertices)
    circle_positions = {}
    radius = 1
    angle_step = 2 * np.pi / n

    # Assign positions in a clockwise manner
    for i, node in enumerate(g.vertices):
        theta = i * angle_step
        x = radius * np.cos(theta)
        y = radius * np.sin(theta)
        circle_positions[node] = (x, y)

    # Draw the graph with labels and dark grey nodes
    nx.draw(nx_graph, pos=circle_positions, with_labels=True, node_color='darkgrey')

    # Convert the matplotlib figure to a Tkinter canvas and display
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack()

    # Update the global reference to the new canvas
    canvas_ref = canvas


# Fetch command from the Text widget
def fetch_command():
    return command_text.get("1.0", tk.END).strip()  # Fetch text from the start (1.0) to the end.

def log_command(command):
    log_text.insert(tk.END, command + "\n")  # Append command to the log.
    log_text.yview(tk.END)  # Scroll to the bottom of the log.


def extract_nodes_from_brackets(command):
    if '[' in command and ']' in command:
        nodes_str = command[command.index('[') + 1: command.index(']')]
        nodes = [node.strip() for node in nodes_str.split(",")]
        command = command.split('[')[0].strip()
        return command, nodes
    return command, []

# GUI setup
root = tk.Tk()
root.title("Graph Commands")

command_label = tk.Label(root, text="Enter Command:")
command_label.pack(padx=10, pady=5)

# Change command_entry to Text widget for multi-line support
command_text = tk.Text(root, width=50, height=3) 
command_text.pack(padx=10, pady=5)

# Log message function
def log_message(message):
    timestamp = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    log_text.insert(tk.END, f"{timestamp} {message}\n")
    log_text.see(tk.END)  # Scroll to the latest message

# ... [No change in the earlier parts of the code] ...

def execute_command():
    command = fetch_command()  # Fetch command from the Text widget

    command, nodes_to_induce = extract_nodes_from_brackets(command)

    # Log the fetched command for tracking
    log_command(command)

    try:
        if command.startswith("create_graph"):
            parts = command.split(" ", 2)
            if len(parts) != 3:
                raise ValueError("Invalid format for 'create_graph'.")
            graph_name = parts[1].strip()
            expression = parts[2].strip()
            save_graph_to_file(graph_name, expression)
            log_message(f"Graph '{graph_name}' created with expression '{expression}'.")

        elif command.startswith("visualize_graph"):
            parts = command.split(" ", 1)
            if len(parts) != 2:
                raise ValueError("Invalid format for 'visualize_graph'.")
            graph_name = parts[1].strip()
            g = load_graph_from_file(graph_name)
            if g is None:
                raise ValueError(f"No graph found with name '{graph_name}'.")

            # Induce the subgraph if nodes were specified
            if nodes_to_induce:
                g = g.induce(nodes_to_induce)

            visualize_graph(g)
            log_message(f"Visualized graph '{graph_name}'.")

        elif command.startswith("visualize_expression"):
            expression = command.replace("visualize_expression", "").strip()
            g = parse_graph(expression)

            # Induce the subgraph if nodes were specified
            if nodes_to_induce:
                g = g.induce(nodes_to_induce)

            visualize_graph(g)
            log_message(f"Visualized expression '{expression}'.")

        else:
            log_message(f"Unknown command: {command}")  # Logging unknown commands
            messagebox.showerror("Error", "Unknown command!")
    
    except Exception as e:  # Generic Exception handler to capture all issues
        log_message(f"Error: {e}")  # Log the error
        messagebox.showerror("Error", str(e))  # Show the error in a dialog

# ... [No changes to the remaining parts of the code] ...


execute_button = tk.Button(root, text="Execute", command=execute_command)
execute_button.pack(padx=10, pady=20)

# GUI elements for the log
log_label = tk.Label(root, text="Log:")
log_label.pack(padx=10, pady=5, anchor="w")

log_text = tk.Text(root, width=60, height=10)
log_text.pack(padx=10, pady=5)

root.mainloop()