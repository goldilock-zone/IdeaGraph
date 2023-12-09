from django.shortcuts import render
from django.http import HttpResponse
from .utils import visualize_adjacency_list, merge_adjacency_lists, extract_content_between_braces, ensure_empty_lists, delete_node_and_children, export_links, export, add_node
from .utils import generate_prompt
from bs4 import BeautifulSoup
from .forms import DeleteNodesForm
from .forms import ConnectionForm
from .models import Node
from .forms import NodeForm, PromptGeneratorForm
from .update_nodes import update_database_with_nodes, check_node_consistency
from .utils import update_graph
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
                file.write(str(ensure_empty_lists(adjacency_list)))
            # You can use this structure to further explore and expand on the idea of Indie-Futurisms
            update_graph(adjacency_list, output_file)

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
    new_button.string = 'Add Generated'  # Set the button text
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

    # Notes 

    # Create a new <a> tag with an href attribute (replace '/your-link-url' with the desired URL)
    link_tag_not = soup.new_tag('a', href="{% url 'node_list' %}")

    # Create a new button element
    new_button = soup.new_tag('button')
    new_button.string = 'Notes'  # Set the button text
    link_tag_not.append(new_button)

    # Create a <div> for positioning the button
    div = soup.new_tag('div', style='position: fixed; bottom: 100px; right: 10px;')

    # Append the button to the <div>
    div.append(link_tag_not)

    # Append the <div> to the body of the HTML
    soup.body.append(div)

    # Export 

    # Create a new <a> tag with an href attribute (replace '/your-link-url' with the desired URL)
    link_tag_exp = soup.new_tag('a', href="{% url 'export' %}")

    # Create a new button element
    new_button = soup.new_tag('button')
    new_button.string = 'Export'  # Set the button text
    link_tag_exp.append(new_button)

    # Create a <div> for positioning the button
    div = soup.new_tag('div', style='position: fixed; bottom: 150px; right: 10px;')

    # Append the button to the <div>
    div.append(link_tag_exp)

    # Append the <div> to the body of the HTML
    soup.body.append(div)

    # Prompt Generator 

    # Create a new <a> tag with an href attribute (replace '/your-link-url' with the desired URL)
    link_tag_pg = soup.new_tag('a', href="{% url 'prompt_generator' %}")

    # Create a new button element
    new_button = soup.new_tag('button')
    new_button.string = 'Prompt Generator'  # Set the button text
    link_tag_pg.append(new_button)

    # Create a <div> for positioning the button
    div = soup.new_tag('div', style='position: fixed; bottom: 200px; right: 10px;')

    # Append the button to the <div>
    div.append(link_tag_pg)

    # Append the <div> to the body of the HTML
    soup.body.append(div)

    # Manual Add

    # Create a new <a> tag with an href attribute (replace '/your-link-url' with the desired URL)
    link_tag_ad = soup.new_tag('a', href="{% url 'connection-form' %}")

    # Create a new button element
    new_button = soup.new_tag('button')
    new_button.string = 'Add Node Manually'  # Set the button text
    link_tag_ad.append(new_button)

    # Create a <div> for positioning the button
    div = soup.new_tag('div', style='position: fixed; bottom: 250px; right: 10px;')

    # Append the button to the <div>
    div.append(link_tag_ad)

    # Append the <div> to the body of the HTML
    soup.body.append(div)


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
                file.write(str(ensure_empty_lists(merged_list)))

            merged_list = ensure_empty_lists(merged_list)
            # You can use this structure to further explore and expand on the idea of Indie-Futurisms
            update_graph(merged_list, output_file)
            
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
                deled_list = delete_node_and_children(parent_list, node)

            merged_list = ensure_empty_lists(deled_list)
            # You can use this structure to further explore and expand on the idea of Indie-Futurisms

            with open(output_file, "w") as file:
                file.write(str(ensure_empty_lists(merged_list)))

            update_graph(merged_list, output_file)

            


        else:
            delete_form = DeleteNodesForm() 

    return render(request, 'circle_app/del.html', {'form': delete_form, 'delete_form': nodes_to_delete})


def create_node(request):
    nodes = Node.objects.all()
    if request.method == 'POST':
        form = NodeForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'circle_app/node_list.html', {'nodes': nodes})  # Redirect to the node list page
    else:
        form = NodeForm()
    
    return render(request, 'circle_app/create_node.html', {'form': form})

def node_list(request):
    nodes = Node.objects.all()
    return render(request, 'circle_app/node_list.html', {'nodes': nodes})


def export_page(request):
    # Add any logic or data you need for the export page
    if request.method == 'POST':
        export_links()
        export()
    return render(request, 'circle_app/export.html')

def prompt_generator(request):
    generated_output = ""

    if request.method == 'POST':
        form = PromptGeneratorForm(request.POST)
        if form.is_valid():
            context_directives = form.cleaned_data['context_directives']
            root_node = form.cleaned_data['root_node']
            depth = form.cleaned_data['depth']
            branching = form.cleaned_data['branching']

            # Call a function to generate output based on form fields
            generated_output = generate_prompt(context_directives, root_node, depth, branching)  # Replace with your actual function
    else:
        form = PromptGeneratorForm()

    return render(request, 'circle_app/prompt_generator.html', {
        'form': form,
        'generated_output': generated_output,
    })

def connection_form(request):
    check_node_consistency(output_file)
    if request.method == 'POST':
        form = ConnectionForm(request.POST)
        if form.is_valid():
            # Process the data, for example, save it or send it somewhere
            node = form.cleaned_data['node']
            selected_options = form.cleaned_data.get('options', [])
            selected_option_names = [node.name for node in selected_options]
            
            with open("circle_app/txtdb/adj_list.txt", 'r') as file:
                fileread = file.read()
            
            parent_list = eval(fileread)
            parent_list = add_node(parent_list, node, selected_option_names)
            
            update_graph(parent_list, output_file)
            

            form.save()
    else:
        form = ConnectionForm()

    check_node_consistency(output_file)
    return render(request, 'circle_app/connection_form.html', {'form': form})


def circle_page(request):
    return render(request, 'circle_app/circle_page.html')