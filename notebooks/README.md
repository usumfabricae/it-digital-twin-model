# Jupyter Notebook Analysis Guide

## Quick Start

### Option 1: Use the Python Script (Easiest)

1. **Start Jupyter Notebook**:
   ```bash
   jupyter notebook
   ```

2. **Create a new notebook** in the `notebooks/` directory

3. **Copy and paste cells** from `ontology_visualization.py` into your notebook
   - Each section marked with `# CELL X:` is a separate cell
   - Copy one section at a time

4. **Run cells sequentially** (Shift+Enter)

### Option 2: Create Notebook from Scratch

Follow the structure in `ontology_visualization.py` but create cells manually.

---

## Installation

### Install Required Packages

```bash
pip install rdflib pandas matplotlib networkx pyvis plotly openpyxl
```

Or create a requirements file:

```bash
# notebooks/requirements.txt
rdflib>=6.0.0
pandas>=1.3.0
matplotlib>=3.4.0
networkx>=2.6.0
pyvis>=0.3.0
plotly>=5.0.0
openpyxl>=3.0.0
```

Then install:
```bash
pip install -r notebooks/requirements.txt
```

---

## Notebook Structure

The notebook is organized into 16 cells:

### Setup Cells (1-4)
1. **Introduction** - Overview and setup instructions
2. **Import Libraries** - Load required Python packages
3. **Define Namespaces** - Set up RDF namespaces
4. **Helper Functions** - Utility functions for queries and visualization

### Query Cells (5-7, 12-13)
5. **Query 1**: List all applications
6. **Query 2**: Physical infrastructure by location
7. **Query 3**: Application dependencies
12. **Query 4**: Full stack decomposition
13. **Query 5**: Layer 4 only

### Visualization Cells (8-11, 14)
8. **Viz 1**: Applications by type (pie chart)
9. **Viz 2**: Infrastructure by location (bar chart)
10. **Viz 3**: Resource distribution (grouped bar chart)
11. **Viz 4**: Dependency network graph (interactive)
14. **Viz 5**: Layer 4 network (interactive)

### Analysis Cells (15-16)
15. **Statistics Summary** - Overall statistics
16. **Export Results** - Save to Excel and CSV

---

## Example Queries

### Query All Applications

```python
query = """
PREFIX : <http://example.org/it-infrastructure-ontology#>

SELECT ?app ?name ?type ?status
WHERE {
  ?app a :Application ;
       :name ?name ;
       :application_type ?type ;
       :lifecycle_status ?status .
}
ORDER BY ?name
"""

df = query_to_dataframe(g, query)
df
```

### Query Layer 4 Infrastructure

```python
query = """
PREFIX : <http://example.org/it-infrastructure-ontology#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?name ?type ?location
WHERE {
  ?entity a ?type .
  ?type rdfs:subClassOf* :PhysicalInfrastructureLayer .
  ?entity :name ?name .
  OPTIONAL { ?entity :location ?location }
}
ORDER BY ?location ?name
"""

df = query_to_dataframe(g, query)
df
```

### Query Dependencies

```python
query = """
PREFIX : <http://example.org/it-infrastructure-ontology#>

SELECT ?app ?appName ?db ?dbName
WHERE {
  ?app a :Application ;
       :name ?appName ;
       :uses ?db .
  ?db a :Database ;
      :name ?dbName .
}
"""

df = query_to_dataframe(g, query)
df
```

---

## Visualizations

### 1. Pie Chart - Applications by Type

```python
import plotly.express as px

app_types = df_apps['type'].value_counts()
fig = px.pie(values=app_types.values, names=app_types.index,
             title='Applications by Type')
fig.show()
```

### 2. Bar Chart - Infrastructure by Location

```python
location_counts = df_infra['location'].value_counts()
fig = px.bar(x=location_counts.index, y=location_counts.values,
             title='Infrastructure by Location')
fig.show()
```

### 3. Interactive Network Graph

```python
from pyvis.network import Network

net = Network(height="750px", width="100%", notebook=True)

# Add nodes and edges
for source, target, label in network_data:
    net.add_node(source, label=source)
    net.add_node(target, label=target)
    net.add_edge(source, target, label=label)

net.show("network.html")
```

### 4. NetworkX Graph

```python
import networkx as nx
import matplotlib.pyplot as plt

G = nx.DiGraph()
for source, target, label in network_data:
    G.add_edge(source, target, label=label)

plt.figure(figsize=(15, 10))
pos = nx.spring_layout(G, k=2, iterations=50)
nx.draw(G, pos, with_labels=True, node_color='lightblue',
        node_size=3000, font_size=8, arrows=True)
plt.title("Dependency Graph")
plt.show()
```

---

## Advanced Queries

### Root Cause Analysis

```python
query = """
PREFIX : <http://example.org/it-infrastructure-ontology#>

SELECT ?component ?layer ?status
WHERE {
  :OrderManagementApp (:uses|:runs_on|:hosted_on|:communicates_via)+ ?component .
  ?component a ?layer ;
             :lifecycle_status ?status .
  FILTER(?status IN ("degraded", "failed"))
}
"""

df = query_to_dataframe(g, query)
df
```

### Impact Analysis

```python
query = """
PREFIX : <http://example.org/it-infrastructure-ontology#>

SELECT ?affected ?type
WHERE {
  ?affected (:runs_on|:hosted_on|:uses)+ :OnPremServer01 ;
            a ?type .
}
"""

df = query_to_dataframe(g, query)
df
```

### Resource Utilization

```python
query = """
PREFIX : <http://example.org/it-infrastructure-ontology#>

SELECT ?location 
       (SUM(?vcpu) AS ?totalVCPU) 
       (SUM(?memory) AS ?totalMemory)
WHERE {
  ?entity :location ?location .
  OPTIONAL { ?entity :vcpu_count ?vcpu }
  OPTIONAL { ?entity :memory_gb ?memory }
}
GROUP BY ?location
ORDER BY DESC(?totalVCPU)
"""

df = query_to_dataframe(g, query)
df
```

---

## Tips and Tricks

### 1. Filter Large Results

```python
# Show only first 20 rows
df.head(20)

# Filter by condition
df[df['status'] == 'production']

# Search for specific text
df[df['name'].str.contains('Azure', case=False)]
```

### 2. Group and Aggregate

```python
# Count by type
df.groupby('type').size()

# Sum resources by location
df.groupby('location')['vcpu'].sum()

# Multiple aggregations
df.groupby('location').agg({
    'vcpu': 'sum',
    'memory': 'sum',
    'name': 'count'
})
```

### 3. Export Specific Results

```python
# Export to CSV
df_apps.to_csv('applications.csv', index=False)

# Export to Excel with multiple sheets
with pd.ExcelWriter('results.xlsx') as writer:
    df_apps.to_excel(writer, sheet_name='Apps')
    df_infra.to_excel(writer, sheet_name='Infrastructure')
```

### 4. Custom Visualizations

```python
# Customize colors
fig = px.bar(df, x='location', y='count',
             color='type',
             color_discrete_sequence=px.colors.qualitative.Set3)

# Add annotations
fig.add_annotation(text="Production Only",
                  xref="paper", yref="paper",
                  x=0.5, y=1.1, showarrow=False)

# Update layout
fig.update_layout(
    title="Custom Title",
    xaxis_title="X Axis",
    yaxis_title="Y Axis",
    font=dict(size=14)
)
```

---

## Troubleshooting

### Issue: Module not found

```bash
pip install <module-name>
```

### Issue: Graph is empty

Check file paths:
```python
import os
print(os.getcwd())  # Check current directory
print(os.path.exists("../ontology/sample-data-complex-hybrid.ttl"))
```

### Issue: Query returns no results

Check namespaces:
```python
# Print all namespaces in graph
for ns_prefix, namespace in g.namespaces():
    print(f"{ns_prefix}: {namespace}")
```

### Issue: Visualization not showing

For Jupyter:
```python
# Enable inline plotting
%matplotlib inline

# For Plotly
import plotly.io as pio
pio.renderers.default = "notebook"
```

---

## Example Workflow

1. **Load data** (Cell 3)
2. **Run a query** (Cell 5-7)
3. **Visualize results** (Cell 8-11)
4. **Analyze** (Cell 15)
5. **Export** (Cell 16)
6. **Iterate** - Modify queries and re-run

---

## Output Files

The notebook generates:

- `dependency_network.html` - Interactive dependency graph
- `layer4_network.html` - Interactive Layer 4 graph
- `ontology_analysis_results.xlsx` - All results in Excel
- `applications.csv` - Application data
- `infrastructure.csv` - Infrastructure data
- `dependencies.csv` - Dependency data

---

## Next Steps

1. **Customize queries** for your specific needs
2. **Create new visualizations** with different chart types
3. **Add filters** to focus on specific components
4. **Export results** for presentations
5. **Share notebooks** with your team

---

**Last Updated**: 2024-01-15  
**Status**: Ready to use

