# This script is also designed to demonstrate the process of visualizing
# a social network using NetworkX and matplotlib in Python.
# It consumes predefined JSON data, but in the real world example data
# from survey data / database and with includes information about
# individuals ('people') and their relationships. The script constructs
# a graph where nodes represent individuals, enriched with attributes
# such as age and occupation, and edges represent the relationships between
# these individuals, including the type and strength of each relationship.
# The visualization highlights the nodes in different colors based on their
# occupation, providing a clear and distinct view of the network structure.
# Additionally, it showcases how to display node and edge attributes
# (like age and relationship type) directly on the graph.


import networkx as nx
import matplotlib.pyplot as plt
import json  # cuz we need to read some JSON

# Let's dive into that JSON, shall we?
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

# Of course, we need to ensure parsing of JSON with error handling as we did in network_metrics.py
data = json.loads(json_data)  # let's get that data ready

# Time to whip up a new graph
G = nx.Graph()

# Throwing in nodes with some juicy details from JSON
for person in data['people']:
    G.add_node(person['name'], age=person['age'], occupation=person['occupation'])

# And let's link 'em up based on those relationships
for rel in data['relationships']:
    G.add_edge(rel['person1'], rel['person2'], relationship=rel['type'], strength=rel['strength'])

# Gonna lay out our network now
pos = nx.spring_layout(G)  # figuring out where everyone goes

# Let's add a splash of color based on what they do
occupation_color = {"Software Developer": "skyblue", "Graphic Designer": "lightgreen", "Project Manager": "salmon"}
node_colors = [occupation_color[G.nodes[node]['occupation']] for node in G.nodes]

# Now, let's make those nodes pop with color
nx.draw(G, pos, with_labels=True, node_color=node_colors, edge_color='gray')

# Don't forget about adding a little note for their age
node_labels = nx.get_node_attributes(G, 'age')
nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=12, font_color='red')

# And what about how they're connected? Let's label those edges too
edge_labels = nx.get_edge_attributes(G, 'relationship')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

plt.show()  # Showtime! Let's see this masterpiece
