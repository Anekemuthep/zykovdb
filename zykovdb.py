import tkinter as tk
from tkinter import messagebox
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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

def v(node_name):
    return Graph({node_name}, set())

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
    # Convert the Graph object to a networkx Graph
    nx_graph = nx.Graph()
    nx_graph.add_nodes_from(g.vertices)
    nx_graph.add_edges_from(g.edges)
    
    # Create a new figure
    fig = plt.figure()

    # Draw the graph with labels
    pos = nx.spring_layout(nx_graph)
    nx.draw(nx_graph, pos, with_labels=True)

    # Convert the matplotlib figure to a Tkinter canvas and display
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack()

def execute_command():
    command = command_entry.get()
    
    if "create_graph" in command:
        try:
            parts = command.split('"')
            graph_name = parts[1]
            expression = parts[2].strip()
            save_graph_to_file(graph_name, expression)
            messagebox.showinfo("Success", f"Graph '{graph_name}' created successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Invalid command format for create_graph! {e}")
    
    elif "visualize_graph" in command:
        try:
            parts = command.split('"')
            graph_name = parts[1]
            g = load_graph_from_file(graph_name)
            if g:
                visualize_graph(g)
            else:
                messagebox.showerror("Error", f"Graph '{graph_name}' not found!")
        except Exception as e:
            messagebox.showerror("Error", f"Invalid command format for visualize_graph! {e}")
    else:
        messagebox.showerror("Error", "Unknown command!")

# GUI setup
root = tk.Tk()
root.title("Graph Commands")

command_label = tk.Label(root, text="Enter Command:")
command_label.pack(padx=10, pady=5)

command_entry = tk.Entry(root, width=50)
command_entry.pack(padx=10, pady=5)

execute_button = tk.Button(root, text="Execute", command=execute_command)
execute_button.pack(padx=10, pady=20)

root.mainloop()