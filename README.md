# zykovdb
A pyhon engine for zykov algebra to create  data graphs and visualize them.

## About zykovDb

The `zykovDb` library is inspired by A. A. Zykov's  1949 fascinating algebraic approach to graph theory. With the wide capabilities of Python, this library breathes life into graph expressions, offering an intuitive way to interact with and visualize them.

### Features:
- 🚀 **Simple Operations**: Effortlessly perform graph algebraic operations like addition and multiplication.
- 📊 **Visualization**: Witness the beauty of your algebraic graph expressions brought to life.
- 💡 **Intuitive Parsing**: Translate human-friendly graph expressions into machine-understandable structures.
  
### Use Cases:
Whether you're a mathematician trying to visualize complex graph structures or a developer wanting to integrate algebraic graph operations into your app, `zykovDb` is your key to unlock the rich world of graph algebra.

# Graph Algebra Toolkit

This toolkit provides a unique way of representing and visualizing graphs using algebraic expressions. Through a simple GUI interface, users can define graphs using a custom algebra and then visualize them.

## Basics of the Graph Algebra

In our custom algebra, a vertex is represented by its name (e.g., "bob"), and edges between vertices are expressed using operators.

### Operators:

- **Addition (`+`)**: Represents the union of two graphs.
- **Multiplication (`*`)**: Represents the link of two graphs.

### Expressions:

1. Individual vertices: `bob`
2. Edge between two vertices: `bob * alice`
3. Union of two graphs: `bob * alice + alice * john`

Complex expressions using parentheses are also supported. For instance: `bob * (alice + john)`

## Commands:

1. **create_graph**: Define and save a graph.
   ```
   create_graph "graph_name" expression
   ```
   Example:
   ```
   create_graph "my_graph" bob * alice + alice * john
   ```

2. **visualize_graph**: Visualize a previously saved graph.
   ```
   visualize_graph "graph_name"
   ```
   Example:
   ```
   visualize_graph "my_graph"
   ```
<img width="634" alt="imageZykovDB2" src="https://github.com/Anekemuthep/zykovdb/assets/31625027/2d1903a9-acf5-4929-aef8-bbebb9fd4e37">

   
3. **visualize_expression**: Visualize a written graph expression.
   ```
   visualize_expression expression
   ```
   Example:
   ```
   visualize_graph bob * (alice + john) + alice * john * norbert
   ```
   
## GUI Usage:

1. Open the GUI application.
2. Type your command in the text box.
3. Click the "Execute" button to run the command.

## Installation

To run this toolkit, you need to have Python installed on your system along with the following libraries:

- `tkinter` for the graphical user interface
- `networkx` and `matplotlib` for graph visualization

You can install the required libraries using pip:

```bash
pip install networkx matplotlib
```

## Contributions

Feel free to open an issue or pull request if you'd like to contribute or suggest changes. Your feedback and contributions are highly appreciated!

## License

This project is open source and available under the [MIT License](LICENSE).

