# circle_app/forms.py
from django import forms
from .models import Node

adjacency_list_file = "circle_app/txtdb/adj_list.txt"
class AdjacencyListForm(forms.Form):
    adjacency_list = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 40}))

class ChildAdjacencyListForm(forms.Form):
    child_adjacency_list = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 40}))
    link_node = forms.CharField(widget=forms.Textarea(attrs={'rows': 2, 'cols': 40}))
    delete_node = forms.CharField(widget=forms.Textarea(attrs={'rows': 2, 'cols': 40}))
    
class DeleteNodesForm(forms.Form):
    nodes_to_delete = forms.CharField(
        label='Nodes to Delete',
        widget=forms.TextInput(attrs={'placeholder': 'Enter nodes to delete (comma-separated)'}),
        required=False  # You can set this to True if deletion is mandatory
    )

class PromptGeneratorForm(forms.Form):
    context_directives = forms.CharField(label='Context Directives', required=True)
    root_node = forms.CharField(label='Root Node', required=True)
    depth = forms.IntegerField(label='Depth', required=True, min_value=1)
    branching = forms.IntegerField(label='Branching', required=True, min_value=1)
class NodeForm(forms.ModelForm):
    class Meta:
        model = Node
        fields = ['name', 'link']
    
    def clean_name(self):
        name = self.cleaned_data['name']
        # Check if a node with the same name already exists in the database
        if Node.objects.filter(name=name).exists():
            return name  # Name exists, return it as is
        else:
            # Name does not exist, raise a validation warning
            raise forms.ValidationError('Warning: This name does not exist in the database.')
