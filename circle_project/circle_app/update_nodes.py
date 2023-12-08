import os
from django.conf import settings
from circle_app.models import Node  # Replace 'your_app' with your app name

def update_database_with_nodes(adjacency_list_file):
    with open(adjacency_list_file, 'r') as file:
        adjacency_list = eval(file.read())

    nodes = set()
    for node, addresses in adjacency_list.items():
        nodes.add(node)
    
    # Update the database with nodes
    existing_nodes = set(Node.objects.values_list('name', flat=True))
    new_nodes = nodes - existing_nodes

    for node_name in new_nodes:
        Node.objects.create(name=node_name)


def check_node_consistency(adjacency_list_file):
    with open(adjacency_list_file, 'r') as file:
        adjacency_list = eval(file.read())

    nodes = []
    for node, addresses in adjacency_list.items():
        nodes.append(node)

    matching_nodes = Node.objects.exclude(name__in=nodes)
    print(matching_nodes)
    matching_nodes.delete()



if __name__ == '__main__':
    # Specify the path to your adjacency list file
    adjacency_list_file = os.path.join(settings.BASE_DIR, 'path_to_adjacency_list.txt')

    # Call the function to update the database with nodes
    update_database_with_nodes(adjacency_list_file)

