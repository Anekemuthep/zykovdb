# zykovdb
A pyhon engine for zykov algebra to create  data graphs and visualize them

# Graph Algebra Toolkit

This toolkit provides a unique way of representing and visualizing graphs using algebraic expressions. Through a simple GUI interface, users can define graphs using a custom algebra and then visualize them.

## Basics of the Graph Algebra

In our custom algebra, a vertex is represented by its name (e.g., "bob"), and edges between vertices are expressed using operators.

### Operators:

- **Addition (`+`)**: Represents the union of two graphs.
- **Multiplication (`*`)**: Represents the product of two graphs.

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

