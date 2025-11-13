# Jupyter Notebook Examples

## Copy-Paste Ready Examples

These examples are ready to copy into Jupyter notebook cells.

---

## Example 1: Basic Setup and Query

```python
# Import libraries
from rdflib import Graph, Namespace, RDF
import pandas as pd

# Define namespaces
ONT = Namespace("http://example.org/it-infrastructure-ontology#")
INST = Namespace("http://example.org/instances#")

# Load data
g = Graph()
g.parse("../ontology/sample-data-complex-hybrid.ttl", format="turtle")
print(f"✓ Loaded {len(g)} triples")

# Simple query
query = """
PREFIX : <http://example.org/it-infrastructure-ontology#>
SELECT ?name ?type WHERE {
  ?app a :Application ;
       :name ?name ;
       :application_type ?type .
}
ORDER BY ?name
"""

# Execute and display
results = g.query(query)
df = pd.DataFrame(results, columns=['name', 'type'])
print(f"Found {len(df)} applications:")
df
```

---

## Example 2: Visualize with Plotly

```python
import plotly.express as px

# Count by type
type_counts = df['type'].value_counts()

# Create pie chart
fig = px.pie(
    values=type_counts.values,
    names=type_counts.index,
    title='Applications by Type',
    color_discrete_sequence=px.colors.qualitative.Pastel
)
fig.update_traces(textposition='inside', textinfo='percent+label')
fig.show()
```

---

## Example 3: Infrastructure Analysis

```python
# Query infrastructure
query_infra = """
PREFIX : <http://example.org/it-infrastructure-ontology#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?name ?type ?location ?vcpu ?memory
WHERE {
  ?entity a ?type .
  ?type rdfs:subClassOf* :PhysicalInfrastructureLayer .
  ?entity :name ?name .
  OPTIONAL { ?entity :location ?location }
  OPTIONAL { ?entity :vcpu_count ?vcpu }
  OPTIONAL { ?entity :memory_gb ?memory }
}
ORDER BY ?location ?name
"""

results = g.query(query_infra)
df_infra = pd.DataFrame(results, columns=['name', 'type', 'location', 'vcpu', 'memory'])

# Show summary
print(f"Total infrastructure: {len(df_infra)} components")
print(f"\nBy location:")
print(df_infra.groupby('location').size())

df_infra
```

---

## Example 4: Resource Summary by Location

```python
import plotly.graph_objects as go

# Calculate totals
resource_summary = df_infra.groupby('location').agg({
    'vcpu': 'sum',
    'memory': 'sum'
}).fillna(0)

# Create grouped bar chart
fig = go.Figure(data=[
    go.Bar(name='vCPU', x=resource_summary.index, y=resource_summary['vcpu']),
    go.Bar(name='Memory (GB)', x=resource_summary.index, y=resource_summary['memory'])
])

fig.update_layout(
    title='Compute Resources by Location',
    xaxis_title='Location',
    yaxis_title='Resources',
    barmode='group',
    xaxis_tickangle=-45,
    height=500
)
fig.show()
```

---

## Example 5: Dependency Network

```python
from pyvis.network import Network

# Query dependencies
query_deps = """
PREFIX : <http://example.org/it-infrastructure-ontology#>

SELECT ?appName ?depName ?relType
WHERE {
  ?app a :Application ;
       :name ?appName .
  
  {
    ?app :uses ?dep .
    BIND("uses" AS ?relType)
  } UNION {
    ?app :calls ?dep .
    BIND("calls" AS ?relType)
  }
  
  ?dep :name ?depName .
}
"""

results = g.query(query_deps)
df_deps = pd.DataFrame(results, columns=['appName', 'depName', 'relType'])

# Create network
net = Network(height="600px", width="100%", notebook=True, bgcolor="#ffffff")

# Add nodes and edges
for _, row in df_deps.iterrows():
    net.add_node(str(row['appName']), label=str(row['appName']), color='lightblue')
    net.add_node(str(row['depName']), label=str(row['depName']), color='lightgreen')
    net.add_edge(str(row['appName']), str(row['depName']), 
                title=str(row['relType']), label=str(row['relType']))

# Configure physics
net.set_options("""
{
  "physics": {
    "enabled": true,
    "stabilization": {"iterations": 100}
  }
}
""")

net.show("dependencies.html")
print("✓ Network saved to dependencies.html")
```

---

## Example 6: Full Stack Trace

```python
# Query full stack
query_stack = """
PREFIX : <http://example.org/it-infrastructure-ontology#>

SELECT ?business ?app ?container ?vm ?server
WHERE {
  ?bp a :BusinessProcess ;
      :name ?business ;
      :realized_by ?application .
  
  ?application :name ?app .
  
  OPTIONAL {
    ?application :deployed_as ?pod .
    ?pod :name ?container .
    ?pod :runs_on ?vmEntity .
    ?vmEntity :name ?vm .
  }
  
  OPTIONAL {
    ?vmEntity :runs_on ?hypervisor .
    ?hypervisor :runs_on ?serverEntity .
    ?serverEntity :name ?server .
  }
}
"""

results = g.query(query_stack)
df_stack = pd.DataFrame(results, 
                       columns=['business', 'app', 'container', 'vm', 'server'])

print("Full Stack Decomposition:")
df_stack
```

---

## Example 7: Filter and Export

```python
# Filter production applications
prod_apps = df[df['status'] == 'production']

# Export to Excel with multiple sheets
with pd.ExcelWriter('analysis_results.xlsx') as writer:
    df.to_excel(writer, sheet_name='All Applications', index=False)
    prod_apps.to_excel(writer, sheet_name='Production Only', index=False)
    df_infra.to_excel(writer, sheet_name='Infrastructure', index=False)
    df_deps.to_excel(writer, sheet_name='Dependencies', index=False)

print("✓ Exported to analysis_results.xlsx")

# Also export to CSV
df.to_csv('applications.csv', index=False)
df_infra.to_csv('infrastructure.csv', index=False)
print("✓ CSV files created")
```

---

## Example 8: Interactive Filtering

```python
from ipywidgets import interact, Dropdown

# Create interactive filter
@interact
def filter_apps(
    app_type=Dropdown(options=['All'] + list(df['type'].unique()), value='All'),
    status=Dropdown(options=['All'] + list(df['status'].unique()), value='All')
):
    filtered = df.copy()
    
    if app_type != 'All':
        filtered = filtered[filtered['type'] == app_type]
    
    if status != 'All':
        filtered = filtered[filtered['status'] == status]
    
    print(f"Showing {len(filtered)} of {len(df)} applications")
    return filtered
```

---

## Example 9: Heatmap Visualization

```python
import seaborn as sns
import matplotlib.pyplot as plt

# Create pivot table
pivot = df_infra.pivot_table(
    values='vcpu',
    index='type',
    columns='location',
    aggfunc='sum',
    fill_value=0
)

# Create heatmap
plt.figure(figsize=(12, 6))
sns.heatmap(pivot, annot=True, fmt='.0f', cmap='YlOrRd', cbar_kws={'label': 'vCPU'})
plt.title('vCPU Distribution by Type and Location')
plt.xlabel('Location')
plt.ylabel('Infrastructure Type')
plt.tight_layout()
plt.show()
```

---

## Example 10: Statistics Dashboard

```python
# Create comprehensive statistics
print("="*60)
print("INFRASTRUCTURE STATISTICS DASHBOARD")
print("="*60)

# Applications
print(f"\n📱 APPLICATIONS")
print(f"  Total: {len(df)}")
print(f"  By Type:")
for app_type, count in df['type'].value_counts().items():
    print(f"    - {app_type}: {count}")

# Infrastructure
print(f"\n🖥️  INFRASTRUCTURE")
print(f"  Total Components: {len(df_infra)}")
print(f"  By Location:")
for location, count in df_infra['location'].value_counts().items():
    print(f"    - {location}: {count}")

# Resources
total_vcpu = df_infra['vcpu'].sum()
total_memory = df_infra['memory'].sum()
print(f"\n📊 RESOURCES")
print(f"  Total vCPU: {total_vcpu:.0f}")
print(f"  Total Memory: {total_memory:.0f} GB")

# Dependencies
print(f"\n🔗 DEPENDENCIES")
print(f"  Total Relationships: {len(df_deps)}")
print(f"  By Type:")
for rel_type, count in df_deps['relType'].value_counts().items():
    print(f"    - {rel_type}: {count}")

print("\n" + "="*60)
```

---

## Example 11: Custom Query Function

```python
def query_ontology(sparql_query, columns=None):
    """
    Execute SPARQL query and return DataFrame.
    
    Args:
        sparql_query: SPARQL query string
        columns: List of column names (optional)
    
    Returns:
        pandas DataFrame with results
    """
    results = g.query(sparql_query)
    
    if columns is None:
        columns = [str(var) for var in results.vars]
    
    data = []
    for row in results:
        data.append([str(row[var]) if row[var] else None for var in results.vars])
    
    df = pd.DataFrame(data, columns=columns)
    print(f"✓ Query returned {len(df)} rows")
    return df

# Usage
my_query = """
PREFIX : <http://example.org/it-infrastructure-ontology#>
SELECT ?name ?status WHERE {
  ?app a :Application ; :name ?name ; :lifecycle_status ?status .
}
"""

df_result = query_ontology(my_query, columns=['Application', 'Status'])
df_result
```

---

## Example 12: Save and Load Analysis

```python
import pickle

# Save your analysis state
analysis_state = {
    'applications': df,
    'infrastructure': df_infra,
    'dependencies': df_deps,
    'timestamp': pd.Timestamp.now()
}

with open('analysis_state.pkl', 'wb') as f:
    pickle.dump(analysis_state, f)

print("✓ Analysis saved to analysis_state.pkl")

# Load later
with open('analysis_state.pkl', 'rb') as f:
    loaded_state = pickle.load(f)

print(f"✓ Analysis loaded from {loaded_state['timestamp']}")
df = loaded_state['applications']
```

---

## Tips

1. **Run cells in order** - Each cell builds on previous ones
2. **Modify queries** - Change SELECT, WHERE, FILTER clauses
3. **Experiment** - Try different visualizations
4. **Save often** - Export results regularly
5. **Document** - Add markdown cells to explain your analysis

---

**Ready to use!** Copy any example into a Jupyter cell and run it.

