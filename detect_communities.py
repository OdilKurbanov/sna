# This script serves as a tool for visualizing social networks and detecting
# community structures within them. Leveraging JSON data that delineates
# individuals and their interconnections, it constructs a graph
# representation of the network.
# Utilizing the Louvain method, the script further analyzes this graph to
# identify and delineate community clusters.
# This approach not only facilitates a deeper understanding of the underlying
# social dynamics but also aids in the visualization of complex relational
# data in a structured and insightful manner.

import networkx as nx
import json
import matplotlib.pyplot as plt
import community as community_louvain  # cool library for community detection

# Let's get that JSON data into something useful, shall we?
def load_data_from_json(json_data):
    """
    Load folks and their connections from JSON stuff.
    """
    try:
        data = json.loads(json_data)
    except json.JSONDecodeError:
        return [], []  # Oopsie, bad JSON
    peeps = data.get('people', [])  # folks we're dealing with
    relations = data.get('relationships', [])  # how they're tied together
    return peeps, relations


# Time to make a graph outta that data
def create_graph_from_data(people, relationships):
    """
    Crafting a graph from peeps and their relations.
    """
    g = nx.Graph()  # Gonna make this a chill, undirected graph
    for person in people:
        g.add_node(person['name'], age=person['age'], job=person['occupation'])

    for relation in relationships:
        g.add_edge(relation['person1'], relation['person2'],
                   type=relation['type'], strength=relation['strength'])
    return g


# Let's see this graph and find some cliques, eh?
def visualize_and_detect_communities(g):
    """
    Drawing the graph and spotting communities with Louvain magic.
    """
    partition = community_louvain.best_partition(g)  # Split 'em up!
    cmap = plt.get_cmap('viridis')  # Fancy colors
    norm = plt.Normalize(0, max(partition.values()))  # Normalize for color mapping
    node_colors = [cmap(norm(value)) for node, value in partition.items()]
    pos = nx.spring_layout(g)  # Where the nodes lie
    nx.draw_networkx_nodes(g, pos, node_color=node_colors, alpha=0.8)
    nx.draw_networkx_edges(g, pos, width=1.0, alpha=0.5)
    nx.draw_networkx_labels(g, pos)
    plt.show()  # Show off that beauty!


# Kicking things off here
if __name__ == "__main__":
    json_data = """
    {
        "people": [
            {"name": "Mahmud Turgay", "age": 30, "occupation": "Software Developer"},
            {"name": "Adam Deniz", "age": 28, "occupation": "Graphic Designer"},
            {"name": "Piter Brown", "age": 35, "occupation": "Project Manager"}
        ],
        "relationships": [
            {"person1": "Mahmud Turgay", "person2": "Adam Deniz", "type": "friends", "strength": "strong"},
            {"person1": "Adam Deniz", "person2": "Piter Brown", "type": "colleagues", "strength": "medium"},
            {"person1": "Piter Brown", "person2": "Mahmud Turgay", "type": "mentor-mentee", "strength": "high"}
        ]
    }
    """
    peeps, relations = load_data_from_json(json_data)  # gettin' data ready
    g = create_graph_from_data(peeps, relations)  # graph's all set
    visualize_and_detect_communities(g)  # let's see what we got!
