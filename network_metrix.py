# This Python script is designed to parse and analyze social network data
# encoded in JSON format, simulating input from a database.
# It constructs a graph representation of individuals and their interrelationships
# using the NetworkX library, enabling detailed analysis and visualization of the
# network's structure. Key features include loading and validating JSON data,
# graph construction with nodes and edges representing people and their
# relationships, respectively, and comprehensive analysis of graph properties
# such as degree distribution, betweenness centrality, and closeness centrality.
# Additionally, it provides functionality for visualizing the network,
# offering insights into the complex interplay of its components.

import networkx as nx
import json
from networkx.readwrite import json_graph
import numpy as np
import matplotlib.pyplot as plt


# Here Simulating JSON data coming from a database
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


def load_data_from_json(json_data):
    """
    Lets load peeps and their relationships from JSON.
    Yeah, we gotta make sure the JSON's legit, or else we're in trouble.
    """
    try:
        data = json.loads(json_data)
    except json.JSONDecodeError:
        raise ValueError("Oops, that JSON's busted.")

    if 'people' not in data or 'relationships' not in data:
        raise ValueError("JSON's gotta have 'people' and 'relationships', or it's no good.")

    people = data['people']
    relationships = data['relationships']
    return people, relationships


def create_graph(people, relationships):
    """
    Time to make that graph! Adding folks and how they're connected.
    """
    g = nx.Graph()
    for person in people:
        g.add_node(person['name'], age=person['age'], occupation=person['occupation'])

    for relationship in relationships:
        g.add_edge(relationship['person1'], relationship['person2'], relationship_type=relationship['type'],
                   strength=relationship['strength'])

    return g


def analyze_graph(g):
    """
    Analyzin' time! Let's see what's up with our graph. Degree distro, betweenness, closeness, the works.
    """
    degrees = [g.degree(n) for n in g.nodes()]
    degree, freq = np.unique(degrees, return_counts=True)
    vertex_betweenness = nx.betweenness_centrality(g, normalized=True)
    closeness = nx.closeness_centrality(g)

    print("Degree distro:", list(zip(degree, freq)))
    print("Betweenness centrality stuff:", vertex_betweenness)
    print("How close are ya:", closeness)


def visualize_graph(g):
    """
    Drawin' time! Let's make this graph look pretty.
    """
    pos = nx.spring_layout(g)
    nx.draw(g, pos, with_labels=True, node_color='skyblue', edge_color='gray')
    plt.show()


# Assuming json_data is defined as in the original code

people, relationships = load_data_from_json(json_data)
g = create_graph(people, relationships)
analyze_graph(g)
# visualize_graph(g)  # Uncomment to see the magic happen
