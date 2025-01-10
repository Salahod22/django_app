from django.shortcuts import render, redirect
from django.core.files.storage import default_storage
from .models import CSVData
from .forms import CSVUploadForm
import pandas as pd
import json
import plotly.express as px

def dashboard(request):
    context = {}
    context['data_entries'] = CSVData.objects.all()  
    return render(request, 'dashboard.html', context)

def upload(request):
    if request.method == 'POST' and 'csv_file' in request.FILES:
        csv_file = request.FILES['csv_file']
        try:
            CSVData.create_from_csv(csv_file)
            message = "File uploaded and processed successfully!"
        except Exception as e:
            message = f"Error processing file: {e}"
        return render(request, 'dashboard.html', {'message': message, 'data_entries': CSVData.objects.all()})
    return redirect('dashboard')

def access_data(request, entry_id):
    entry = CSVData.objects.get(id=entry_id)
    try:
        # Load data
        data = json.loads(entry.data) if isinstance(entry.data, str) else entry.data
        df = pd.DataFrame(data)
    except Exception as e:
        return render(request, 'dashboard.html', {
            'error': f"Error loading data: {e}",
            'data_entries': CSVData.objects.all(),
        })

    if df.empty:
        return render(request, 'dashboard.html', {
            'error': "The dataset is empty or could not be loaded.",
            'data_entries': CSVData.objects.all(),
        })

    # Context
    context = {
        'entry': entry,
        'data_entries': CSVData.objects.all(),
        'columns': df.columns.tolist(),
    }

    # Row Display
    row_index = request.GET.get('row_index')
    if row_index:
        try:
            row_index = int(row_index)
            if 0 <= row_index < len(df):
                context['row_data'] = df.iloc[row_index].to_dict()
                context['row_index'] = row_index
            else:
                context['error'] = f"Row index {row_index} is out of bounds. Valid range: 0 to {len(df) - 1}."
        except ValueError:
            context['error'] = "Invalid row index. Please enter a numeric value."

    # Column Display
    column_name = request.GET.get('column_name')
    if column_name:
        if column_name in df.columns:
            context['column_data'] = df[column_name].tolist()
            context['column_name'] = column_name
        else:
            context['error'] = f"Column '{column_name}' does not exist in the dataset."

    return render(request, 'dashboard.html', context)



# Analyse statistique des données 
def analyze_data(request, entry_id):
    entry = CSVData.objects.get(id=entry_id)
    df = pd.DataFrame(json.loads(entry.data))
    context = {'entry': entry, 
               'data_entries': CSVData.objects.all(),
               'columns': df.columns.tolist()
               }
    stats = {}
    for column in df.columns:
        if pd.api.types.is_numeric_dtype(df[column]):
            stats[column] = {
                'mean': df[column].mean(),
                'median': df[column].median(),
                'std': df[column].std(),
                'min': df[column].min(),
                'max': df[column].max(),
            }
    context['stats'] = stats
    return render(request, 'dashboard.html', context)


#Visualisation des données 
def visualize_data(request, entry_id):
    entry = CSVData.objects.get(id=entry_id)
    df = pd.DataFrame(json.loads(entry.data))
    context = {'entry': entry, 'data_entries': CSVData.objects.all()}

    plot_type = request.GET.get('plot_type', 'histogram')
    column = request.GET.get('column')
    if column and column in df.columns:
        if plot_type == 'histogram':
            fig = px.histogram(df, x=column)
        elif plot_type == 'scatter':
            y_column = request.GET.get('y_column')
            if y_column and y_column in df.columns:
                fig = px.scatter(df, x=column, y=y_column)
            else:
                context['plot_error'] = "Invalid Y-axis column."
        elif plot_type == 'bar':
            fig = px.bar(df, x=column)
        else:
            context['plot_error'] = "Invalid plot type."
        
        if 'fig' in locals():
            context['plot_html'] = fig.to_html(full_html=False)

    return render(request, 'dashboard.html', context)

# List des fichiers téléchargé
def data_list(request):
    data_entries = CSVData.objects.all()
    return render(request, 'dashboard.html', {'data_entries': data_entries})