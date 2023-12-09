import networkx as nx
from pyvis.network import Network
import sqlite3
import os
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import filedialog
# This file should be made object oriented

def visualize_adjacency_list(adjacency_list):

    # Create a directed graph
    G = nx.DiGraph()

    # Add nodes and edges from the adjacency list
    for node, neighbors in adjacency_list.items():
        G.add_node(node)

    # Create a pyvis network
    net = Network(height="1024px", width="100%", notebook=True)

    # Assign random colors to nodes
    node_colors = {node: f"#FFB6C1" for node in adjacency_list}

    # Add nodes with assigned colors to the network
    for node, color in node_colors.items():
        net.add_node(node, color=color)

    # Add edges to the network
    for node, neighbors in adjacency_list.items():
        net.add_edges([(node, neighbor) for neighbor in neighbors])

    # Get the HTML content generated by pyvis.Network
    net.show("circle_app/templates/circle_app/temp.html")

def merge_adjacency_lists(parent_adj_list, child_adj_list, expansion_node, child_connection_node):
    """
    Merges two adjacency lists with a specified connection between a node in the parent graph and a node in the child graph.

    Args:
    - parent_adj_list (dict): The adjacency list of the parent graph.
    - child_adj_list (dict): The adjacency list of the child graph to merge.
    - expansion_node (str): The node in the parent graph where the child graph is to be merged.
    - child_connection_node (str): The node in the child graph to be connected with the expansion node.

    Returns:
    - dict: The merged adjacency list.
    """
    # Check if the expansion node and child connection node exist
    
    if expansion_node not in parent_adj_list:
        raise ValueError(f"Node {expansion_node} not found in the parent adjacency list.")
    if child_connection_node not in child_adj_list:
        raise ValueError(f"Node {child_connection_node} not found in the child adjacency list.")

    # Merge the child adjacency list into the parent adjacency list
    for node, edges in child_adj_list.items():
        if node in parent_adj_list:
            parent_adj_list[node].extend(edges)
        else:
            parent_adj_list[node] = edges

    # Link the expansion node in the parent graph to the specified node in the child graph
    if child_connection_node not in parent_adj_list[expansion_node]:
        parent_adj_list[expansion_node].append(child_connection_node)

    return parent_adj_list

def extract_content_between_braces(input_string):
    # Find the indices of the first "{" and the last "}"
    first_open_brace_index = input_string.find("{")
    last_close_brace_index = input_string.rfind("}")

    # Check if both "{" and "}" were found
    if first_open_brace_index != -1 and last_close_brace_index != -1:
        # Extract the content between the first "{" and the last "}"
        extracted_content = input_string[first_open_brace_index:last_close_brace_index + 1]
        return extracted_content
    else:
        return None
    
def ensure_empty_lists(adjacency_list):
    # Find all nodes that are not keys in the adjacency_list
    all_nodes = set()
    for node, neighbors in adjacency_list.items():
        all_nodes.add(node)
        all_nodes.update(neighbors)

    # Identify leaf nodes (nodes with no outgoing edges)
    leaf_nodes = [node for node in all_nodes if node not in adjacency_list or not adjacency_list[node]]

    # Add empty lists for any leaf nodes missing them
    for leaf_node in leaf_nodes:
        if leaf_node not in adjacency_list:
            adjacency_list[leaf_node] = []

    return adjacency_list

def create_node_string_dictionary(adjacency_list, associated_strings):
    node_strings = {}
    for node in adjacency_list:
        if node in associated_strings:
            node_strings[node] = associated_strings[node]
        else:
            node_strings[node] = "No associated string available for this node."
    return node_strings

def delete_node_and_children(adj_list, node):
    if node not in adj_list:
        return adj_list  # Node not found in the graph, nothing to delete

    # Recursively delete the node and its children
    def delete_recursive(current_node):
        if current_node in adj_list:
            for neighbor in adj_list[current_node]:
                delete_recursive(neighbor)
            print(adj_list[current_node])
            del adj_list[current_node]

    delete_recursive(node)
    # Remove references to the deleted node from other nodes' adjacency lists
    for key in adj_list:
        adj_list[key] = [neighbor for neighbor in adj_list[key] if neighbor != node]

    return adj_list

def export_links():
    # 1. Connect to the SQLite database (replace 'your_database.db' with your database file)
    conn = sqlite3.connect('db.sqlite3')

    # 2. Create a cursor object
    cursor = conn.cursor()

    # 3. Execute a SELECT query (replace 'your_table' with the name of your table)
    cursor.execute('SELECT * FROM circle_app_node')
    
    # Start building the HTML table
    html_table = '<table border="1">\n'
    html_table += '<tr><th>Node</th><th>Link</th></tr>\n'
    # 4. Fetch and display the data
    for row in cursor.fetchall():
        print(row[1:])
        html_table += f'<tr><td>{row[1]}</td><td>{row[2]}</td></tr>\n'

    html_table += '</table>'
    
    html_content = '<!DOCTYPE html>\n<html>\n<head>\n<title>Table Example</title>\n</head>\n<body>\n'
    html_content += html_table
    html_content += '</body>\n</html>'

    with open('temp_export/output.html', 'w') as file:
        file.write(html_content)

    # 5. Close the cursor and connection
    cursor.close()
    conn.close()

def export():
    # Step 1: Read the content of both HTML files
    with open("circle_app/templates/circle_app/temp.html", "r") as left_file:
        left_html = left_file.read()

    left_soup = BeautifulSoup(left_html, 'html.parser')
    for button in left_soup.find_all('button'):
        button.extract()  # Remove the button element

    left_html = str(left_soup)

    with open("temp_export/output.html", "r") as right_file:
        right_html = right_file.read()
   # Step 2: Create a new HTML file
    combined_html = '<div style="width: 75%; float: left;">' + left_html + '</div>'
    combined_html += '<div style="width: 25%; float: right; overflow-y: auto; height: 100vh;">' + right_html + '</div>'

    # Step 3: Open a dialog box to choose the folder
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    folder_path = filedialog.askdirectory(title="Select Folder to Save Combined HTML")

    if folder_path:
        # Step 4: Save the new HTML file to the selected folder
        combined_file_path = os.path.join(folder_path, "combined.html")
        with open(combined_file_path, "w") as combined_file:
            combined_file.write(combined_html)
        print(f"HTML files combined and saved as 'combined.html' in {folder_path}")

     # Step 4: Save the new HTML file
    print("HTML files combined and saved as 'combined.html'")
  

