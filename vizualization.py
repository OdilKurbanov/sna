# This script is designed for the visualization and analysis of social networks,
# leveraging data encoded in JSON format. It loads individuals and their interconnections,
# incorporating them into a graph structure using the NetworkX library.
# The process involves parsing JSON data to extract entities and their relationships,
# dynamically constructing a graph, and finally visualizing the network.
# Additionally, it provides a mechanism for outputting the graph's data in JSON format,
# facilitating further analysis or visualization with external tools.
# This approach not only enhances the understanding of complex social networks
# but also showcases the versatility of Python in handling and representing relational data.


import networkx as nx
import json
from networkx.readwrite import json_graph
import matplotlib.pyplot as plt  # For drawing plots, cuz why not?


# Let's load up some data, shall we?
def load_data_from_json(json_data):
    """
    Load folks and their connections from JSON data.

    Args:
    - json_data: A JSON string with all the juicy details.

    Returns:
    Two lists, one of people and the other of relationships. Simple!
    """
    data = json.loads(json_data)  # Decode that JSON!
    people = data.get('people', [])  # Default to empty if missing
    relationships = data.get('relationships', [])  # Ditto
    return people, relationships


# Now, let's get those people and relationships into our graph
def add_people_and_relationships_from_data(g, people, relationships):
    """
    Throws people and their relationships into the graph.

    Args:
    - g: Graph where the party's at.
    - people: List of dicts, each dict is a person.
    - relationships: List of dicts, each dict is a relationship.
    """
    for person in people:
        add_person(g, person['name'], person['age'], person['occupation'])  # Add each person

    for relationship in relationships:
        add_relationship(g, relationship['person1'], relationship['person2'], relationship['type'],
                         relationship['strength'])  # And their connections


# Adding a single person to the mix
def add_person(g, name, age, occupation):
    g.add_node(name, age=age, occupation=occupation)  # Just slap them into the graph
    return name  # Why not, might be handy


# Linking two folks together
def add_relationship(g, person1, person2, relationship_type, strength):
    g.add_edge(person1, person2, relationship_type=relationship_type, strength=strength)  # Connect 'em


# Let's make our graph look pretty
def visualize_graph(g, output_file="complex_network.json"):
    data = json_graph.node_link_data(g)  # Get the data ready
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=4)  # And save it


# Pretending we got some JSON from a database or something
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

g = nx.Graph()  # Starting off our graph

people, relationships = load_data_from_json(json_data)  # Load 'em up
add_people_and_relationships_from_data(g, people, relationships)  # And add 'em in

# Let's save this masterpiece
visualize_graph(g)

# Uncomment below to test as a visualization part
# def plot_graph(g):
#     # Drawing stuff, making it look good
#     pos = nx.spring_layout(g)  # Lay 'em out
#
#     # Colors for different types of relationships, because variety is the spice of life
#     relationship_colors = {
#         "friend": "blue",
#         "colleague": "green",
#         "neighbor": "red",
#         "mentor": "purple",
#         "consultant": "orange"
#     }
#
#     # Drawing nodes, labels, and colored edges based on relationships
#     nx.draw_networkx_nodes(g, pos, node_size=2000, node_color="lightblue", alpha=0.6)
#     nx.draw_networkx_labels(g, pos, font_size=10, font_weight="bold")
#     for edge in g.edges(data=True):
#         rel_type = edge[2].get('relationship')  # What kinda link they got?
#         color = relationship_colors.get