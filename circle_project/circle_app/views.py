from django.shortcuts import render
from django.http import HttpResponse
from .utils import visualize_adjacency_list, merge_adjacency_lists, extract_content_between_braces, ensure_empty_lists, delete_node_and_children
from bs4 import BeautifulSoup
from .forms import DeleteNodesForm

import os

from .forms import AdjacencyListForm, ChildAdjacencyListForm

output_file = "circle_app/txtdb/adj_list.txt"

def home(request):
    adjacency_list = None
    

    if request.method == 'POST':
        form = AdjacencyListForm(request.POST)
        if form.is_valid():
            
            adjacency_list = extract_content_between_braces(form.cleaned_data['adjacency_list'])
            adjacency_list = eval(adjacency_list)
            with open(output_file, "w") as file:
                file.write(str(adjacency_list))
            # You can use this structure to further explore and expand on the idea of Indie-Futurisms
            visualize_adjacency_list(ensure_empty_lists(adjacency_list))

    else:
        form = AdjacencyListForm()

    return render(request, 'circle_app/home.html', {'form': form, 'adjacency_list': adjacency_list})

def display_html_file(request):
    with open('circle_app/templates/circle_app/temp.html', 'r', encoding='utf-8') as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, 'html.parser')

    # Adding 

    # Create a new <a> tag with an href attribute (replace '/your-link-url' with the desired URL)
    link_tag_add = soup.new_tag('a', href="{% url 'add' %}")

    # Create a new button element
    new_button = soup.new_tag('button')
    new_button.string = 'Add'  # Set the button text
    link_tag_add.append(new_button)

    # Create a <div> for positioning the button
    div = soup.new_tag('div', style='position: fixed; bottom: 10px; right: 10px;')

    # Append the button to the <div>
    div.append(link_tag_add)

    # Append the <div> to the body of the HTML
    soup.body.append(div)

    # Delete

    # Create a new <a> tag with an href attribute (replace '/your-link-url' with the desired URL)
    link_tag_del = soup.new_tag('a', href="{% url 'del' %}")

    # Create a new button element
    new_button = soup.new_tag('button')
    new_button.string = 'Del'  # Set the button text
    link_tag_del.append(new_button)

    # Create a <div> for positioning the button
    div = soup.new_tag('div', style='position: fixed; bottom: 40px; right: 10px;')

    # Append the button to the <div>
    div.append(link_tag_del)

    # Append the <div> to the body of the HTML
    soup.body.append(div)



    print(soup)

    # Save the modified HTML back to a file
    with open('circle_app/templates/circle_app/temp.html', 'w', encoding='utf-8') as file:
        file.write(str(soup))

    return render(request, 'circle_app/temp.html')

def add_page(request):
    child_adjacency_list = None

    if request.method == 'POST':
        form = ChildAdjacencyListForm(request.POST)
        if form.is_valid():
            child_adjacency_list = extract_content_between_braces(form.cleaned_data['child_adjacency_list'])
            link_node = form.cleaned_data['link_node']
            
            with open("circle_app/txtdb/adj_list.txt", 'r') as file:
                parent_list = file.read()
            
            child_adjacency_list = eval(child_adjacency_list)
            parent_adjacency_list = eval(parent_list)

            merged_list = merge_adjacency_lists(parent_adjacency_list, child_adjacency_list, link_node, link_node)
            
            with open(output_file, "w") as file:
                file.write(str(merged_list))

            merged_list = ensure_empty_lists(merged_list)
            # You can use this structure to further explore and expand on the idea of Indie-Futurisms
            visualize_adjacency_list(merged_list)
            
        # Check if the form for deleting nodes is submitted
    
        
            # Parse the child adjacency list (similar to what you did in the home view)
    else:
        form = ChildAdjacencyListForm()
        delete_form = DeleteNodesForm() 



    return render(request, 'circle_app/temp_page.html', {'form': form, 'child_adjacency_list': child_adjacency_list, 'delete_form': delete_form})

def del_page(request):
    delete_form = DeleteNodesForm()
    nodes_to_delete = []
    if request.method == 'POST':
        delete_form = DeleteNodesForm(request.POST)
        if delete_form.is_valid():
            nodes_to_delete = delete_form.cleaned_data['nodes_to_delete']

            with open("circle_app/txtdb/adj_list.txt", 'r') as file:
                parent_list = file.read()

            parent_list = eval(parent_list)
            
            nodes_to_delete = nodes_to_delete.split(',')
            for node in nodes_to_delete:
                parent_list = delete_node_and_children(parent_list, node)

            merged_list = ensure_empty_lists(parent_list)
            # You can use this structure to further explore and expand on the idea of Indie-Futurisms
            visualize_adjacency_list(merged_list)


        else:
            delete_form = DeleteNodesForm() 

    return render(request, 'circle_app/del.html', {'form': delete_form, 'delete_form': nodes_to_delete})

# Create your views here.
def circle_page(request):
    return render(request, 'circle_app/circle_page.html')