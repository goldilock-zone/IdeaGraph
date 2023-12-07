# circle_app/forms.py
from django import forms

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