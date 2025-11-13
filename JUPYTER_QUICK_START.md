# Jupyter Notebook Quick Start Guide

## Yes! Jupyter is Perfect for This

Jupyter notebooks are excellent for querying and visualizing RDF/ontology data. You get:

- ✅ Interactive queries with immediate results
- ✅ Beautiful visualizations (charts, graphs, networks)
- ✅ Easy data exploration and filtering
- ✅ Export results to Excel, CSV, HTML
- ✅ Share analysis with your team
- ✅ Iterate quickly on queries

---

## Quick Setup (3 Steps)

### Step 1: Install Packages

```bash
pip install rdflib pandas matplotlib networkx pyvis plotly openpyxl jupyter
```

### Step 2: Start Jupyter

```bash
cd notebooks
jupyter notebook
```

### Step 3: Create Notebook

1. Click "New" → "Python 3"
2. Copy cells from `ontology_visualization.py`
3. Run cells with Shift+Enter

---

## What You'll Get

### 📊 Interactive Queries

Query your ontology with SPARQL and see results as DataFrames:

```python
query = """
SELECT ?app ?name ?type
WHERE {
  ?app a :Application ;
       :name ?name ;
       :application_type ?type .
}
"""
df = query_to_dataframe(g, query)
df  # Beautiful table output
```

### 📈 Visualizations

**Pie Charts** - Application distribution:
```python
fig = px.pie(values=counts, names=labels, title='Apps by Type')
fig.show()
```

**Bar Charts** - Infrastructure by location:
```python
fig = px.bar(x=locations, y=counts, title='Infrastructure')
fig.show()
```

**Network Graphs** - Interactive dependency visualization:
```python
net = Network(height="750px", notebook=True)
net.add_nodes(nodes)
net.add_edges(edges)
net.show("network.html")
```

### 📑 Data Export

Export to multiple formats:
```python
df.to_csv('results.csv')
df.to_excel('results.xlsx')
df.to_html('results.html')
```

---

## Example Notebook Structure

```
Cell 1: Import libraries
Cell 2: Load ontology data
Cell 3: Query applications
Cell 4: Visualize with pie chart
Cell 5: Query infrastructure
Cell 6: Visualize with bar chart
Cell 7: Query dependencies
Cell 8: Create network graph
Cell 9: Export results
```

---

## Pre-Built Queries Included

### 1. List All Applications
```python
# Returns: app name, type, deployment model, status
```

### 2. Physical Infrastructure by Location
```python
# Returns: location, type, name, vCPU, memory
```

### 3. Application Dependencies
```python
# Returns: app, dependency, relationship type
```

### 4. Full Stack Decomposition
```python
# Returns: business process → app → container → infrastructure
```

### 5. Layer 4 Only
```python
# Returns: all physical infrastructure components
```

---

## Visualizations Included

### 1. Pie Chart - Applications by Type
Shows distribution of microservices vs legacy vs SOA

### 2. Bar Chart - Infrastructure by Location
Compares on-premises vs Azure vs AWS

### 3. Grouped Bar Chart - Resources by Location
Shows vCPU and memory distribution

### 4. Interactive Network - Dependencies
Click and drag to explore application dependencies

### 5. Interactive Network - Layer 4
Visualize physical infrastructure relationships

---

## Files Created for You

```
notebooks/
├── README.md                      # Detailed guide
├── ontology_visualization.py      # All code cells
├── setup_jupyter.sh              # Linux/Mac setup
├── setup_jupyter.bat             # Windows setup
└── requirements.txt              # Package list
```

---

## Quick Start Commands

### Windows
```bash
cd notebooks
setup_jupyter.bat
```

### Linux/Mac
```bash
cd notebooks
chmod +x setup_jupyter.sh
./setup_jupyter.sh
```

### Manual
```bash
pip install rdflib pandas matplotlib networkx pyvis plotly openpyxl jupyter
cd notebooks
jupyter notebook
```

---

## Using the Pre-Built Code

### Option 1: Copy-Paste (Easiest)

1. Open `ontology_visualization.py`
2. Copy each section marked `# CELL X:`
3. Paste into new Jupyter cells
4. Run sequentially

### Option 2: Import as Module

```python
# In Jupyter notebook
import sys
sys.path.append('..')
from notebooks.ontology_visualization import *
```

### Option 3: Run as Script

```python
# In Jupyter notebook
%run ontology_visualization.py
```

---

## Example Session

```python
# Cell 1: Setup
from rdflib import Graph, Namespace
import pandas as pd
import plotly.express as px

ONT = Namespace("http://example.org/it-infrastructure-ontology#")
g = Graph()
g.parse("../ontology/sample-data-complex-hybrid.ttl", format="turtle")
print(f"Loaded {len(g)} triples")

# Cell 2: Query applications
query = """
PREFIX : <http://example.org/it-infrastructure-ontology#>
SELECT ?name ?type WHERE {
  ?app a :Application ; :name ?name ; :application_type ?type .
}
"""
results = g.query(query)
df = pd.DataFrame(results, columns=['name', 'type'])
df

# Cell 3: Visualize
counts = df['type'].value_counts()
fig = px.pie(values=counts.values, names=counts.index)
fig.show()

# Cell 4: Export
df.to_excel('applications.xlsx', index=False)
print("✓ Exported to applications.xlsx")
```

---

## Advanced Features

### Filter and Analyze

```python
# Filter by status
prod_apps = df[df['status'] == 'production']

# Group by location
df.groupby('location')['vcpu'].sum()

# Search
df[df['name'].str.contains('Azure')]
```

### Custom Queries

```python
# Your custom SPARQL query
my_query = """
PREFIX : <http://example.org/it-infrastructure-ontology#>
SELECT ?x ?y ?z WHERE {
  # Your query here
}
"""
my_df = query_to_dataframe(g, my_query)
```

### Interactive Exploration

```python
# Click on cells to see details
df.style.highlight_max(axis=0)

# Interactive filtering
from ipywidgets import interact
@interact
def filter_by_type(app_type=['microservice', 'legacy', 'SOA_service']):
    return df[df['type'] == app_type]
```

---

## Output Examples

### Query Output
```
     name                          type           status
0    Customer Service App          microservice   production
1    Order Management App          microservice   production
2    Legacy ERP System             SOA_service    production
3    Payment Service App           microservice   production
4    Inventory Service App         microservice   production
```

### Statistics Output
```
ONTOLOGY STATISTICS SUMMARY
============================================================
Business Processes      :   5 entities
Applications           :  12 entities
Containers             :   6 entities
Infrastructure         :  27 entities
Network                :  10 entities
Security               :  15 entities
============================================================
```

### Network Graph
Interactive HTML file with:
- Clickable nodes
- Draggable layout
- Zoom and pan
- Relationship labels
- Color-coded by type

---

## Tips for Success

### 1. Start Simple
Begin with basic queries, then add complexity

### 2. Use DataFrames
Pandas DataFrames make data manipulation easy

### 3. Visualize Early
Create charts to understand your data

### 4. Save Your Work
Export results and visualizations

### 5. Iterate
Modify queries and re-run cells quickly

---

## Troubleshooting

### Jupyter won't start
```bash
pip install --upgrade jupyter
jupyter notebook --version
```

### Packages not found
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Graph is empty
```python
# Check file path
import os
print(os.getcwd())
print(os.path.exists("../ontology/sample-data-complex-hybrid.ttl"))
```

### Visualization not showing
```python
# For Plotly in Jupyter
import plotly.io as pio
pio.renderers.default = "notebook"
```

---

## Next Steps

1. ✅ Install packages
2. ✅ Start Jupyter
3. ✅ Copy cells from `ontology_visualization.py`
4. ✅ Run and explore
5. ✅ Customize for your needs
6. ✅ Share with team

---

## Resources

- **Code**: `notebooks/ontology_visualization.py`
- **Guide**: `notebooks/README.md`
- **Setup**: `notebooks/setup_jupyter.bat` (Windows) or `.sh` (Linux/Mac)
- **Data**: `ontology/sample-data-complex-hybrid.ttl`

---

**Ready to start?**

```bash
cd notebooks
jupyter notebook
```

Then create a new notebook and start copying cells!

---

**Last Updated**: 2024-01-15  
**Status**: Ready to use

