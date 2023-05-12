import networkx as nx
from pyvis.network import Network

# Define the network elements
as1_routers = ['as1ra', 'as1rb', 'as1rc', 'as1rd']
as2_routers = ['as2ra', 'as2rb', 'as2rc', 'as2rd']
as3_routers = ['as3ra', 'as3rb', 'as3rc', 'as3rd']

as1_hosts = ['h1a', 'h1b', 'h1c', 'h1d']
as2_hosts = ['h2a', 'h2b', 'h2c', 'h2d']
as3_hosts = ['h3a', 'h3b', 'h3c', 'h3d']

         
interfaces = [('as1ra', 'as1rb'), ('as1ra', 'as1rd'), ('as1rb', 'as1rc'),
              ('as1rc', 'as1rd'),
              ('as2ra', 'as2rb'), ('as2ra', 'as2rd'), ('as2rb', 'as2rc'),
              ('as2rc', 'as2rd'),
              ('as3ra', 'as3rb'), ('as3ra', 'as3rd'), ('as3rb', 'as3rc'),
              ('as3rc', 'as3rd'),
              ('as1rc', 'as2ra'), ('as2rc', 'as3ra'), ('as3rc', 'as1ra'),
              ('as1ra', 'h1a'), ('as1rb', 'h1b'), ('as1rc', 'h1c'), ('as1rd', 'h1d'),
              ('as2ra', 'h2a'), ('as2rb', 'h2b'), ('as2rc', 'h2c'), ('as2rd', 'h2d'),
              ('as3ra', 'h3a'), ('as3rb', 'h3b'), ('as3rc', 'h3c'), ('as3rd', 'h3d')]



# Create the network graph and add nodes and edges
G = nx.Graph()
G.add_nodes_from(as1_routers + as2_routers + as3_routers)
G.add_nodes_from(as1_hosts + as2_hosts + as3_hosts)
G.add_edges_from(interfaces)

# Create a PyVis Network and add the NetworkX graph
nt = Network(notebook=True)
nt.from_nx(G)

# Define the different shades of red and green for each AS
as1_router_color = 'green'
as2_router_color = 'red'
as3_router_color = 'blue'

as1_host_color = 'darkgreen'
as2_host_color = 'darkred'
as3_host_color = 'darkblue'

# Customize the node colors and sizes
for node in nt.nodes:
    if node['id'] in as1_routers:
        node['color'] = as1_router_color
        node['size'] = 30
    elif node['id'] in as2_routers:
        node['color'] = as2_router_color
        node['size'] = 30
    elif node['id'] in as3_routers:
        node['color'] = as3_router_color
        node['size'] = 30
    elif node['id'] in as1_hosts:
        node['color'] = as1_host_color
        node['size'] = 20
    elif node['id'] in as2_hosts:
        node['color'] = as2_host_color
        node['size'] = 20
    elif node['id'] in as3_hosts:
        node['color'] = as3_host_color
        node['size'] = 20

for node in nt.nodes:
    print(node['id']+":"+node['color'])

# Enable physics for draggable nodes
nt.toggle_physics(True)

# Show the interactive graph
nt.show('interactive_graph.html')
