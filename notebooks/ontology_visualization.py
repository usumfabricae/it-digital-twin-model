# IT Infrastructure Ontology - Jupyter Notebook Analysis
# Copy this code into Jupyter notebook cells

# ============================================================================
# CELL 1: Install Required Packages (run once)
# ============================================================================
"""
!pip install rdflib pandas matplotlib networkx pyvis plotly
"""

# ============================================================================
# CELL 2: Import Libraries
# ============================================================================

from rdflib import Graph, Namespace, RDF, RDFS
from rdflib.plugins.sparql import prepareQuery
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from pyvis.network import Network
import plotly.graph_objects as go
import plotly.express as px
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

# Set display options
pd.set_option('display.max_rows', 100)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

print("✓ Libraries imported successfully")

# ============================================================================
# CELL 3: Define Namespaces and Load Data
# ============================================================================

# Define namespaces
ONT = Namespace("http://example.org/it-infrastructure-ontology#")
INST = Namespace("http://example.org/instances#")

# Load the ontology and data
g = Graph()
g.parse("../ontology/it-infrastructure-ontology.ttl", format="turtle")
g.parse("../ontology/sample-data-complex-hybrid.ttl", format="turtle")

print(f"✓ Loaded {len(g)} triples")
print(f"  Ontology + Complex Hybrid Architecture")

# ============================================================================
# CELL 4: Helper Functions
# ============================================================================

def query_to_dataframe(graph, sparql_query):
    """Execute SPARQL query and return results as DataFrame."""
    results = graph.query(sparql_query)
    data = []
    for row in results:
        data.append({str(var): str(row[var]) if row[var] else None 
                    for var in results.vars})
    return pd.DataFrame(data)

def get_entity_name(uri):
    """Extract entity name from URI."""
    return str(uri).split('#')[-1].split('/')[-1]

def visualize_network(graph_data, title="Network Visualization", 
                     height="750px", notebook=True):
    """Create interactive network visualization using PyVis."""
    net = Network(height=height, width="100%", 
                 bgcolor="#ffffff", font_color="black", notebook=notebook)
    
    # Add nodes and edges
    for source, target, label in graph_data:
        net.add_node(source, label=source, title=source)
        net.add_node(target, label=target, title=target)
        net.add_edge(source, target, label=label, title=label)
    
    # Configure physics
    net.set_options("""
    {
      "physics": {
        "forceAtlas2Based": {
          "gravitationalConstant": -50,
          "centralGravity": 0.01,
          "springLength": 200,
          "springConstant": 0.08
        },
        "maxVelocity": 50,
        "solver": "forceAtlas2Based",
        "timestep": 0.35,
        "stabilization": {"iterations": 150}
      }
    }
    """)
    
    return net

print("✓ Helper functions defined")

# ============================================================================
# CELL 5: Query 1 - List All Applications
# ============================================================================

query_applications = """
PREFIX : <http://example.org/it-infrastructure-ontology#>
PREFIX inst: <http://example.org/instances#>

SELECT ?app ?name ?type ?deployment ?status
WHERE {
  ?app a :Application ;
       :name ?name ;
       :application_type ?type ;
       :deployment_model ?deployment ;
       :lifecycle_status ?status .
}
ORDER BY ?name
"""

df_apps = query_to_dataframe(g, query_applications)
print(f"Found {len(df_apps)} applications:")
df_apps

# ============================================================================
# CELL 6: Query 2 - Physical Infrastructure by Location
# ============================================================================

query_infrastructure = """
PREFIX : <http://example.org/it-infrastructure-ontology#>
PREFIX inst: <http://example.org/instances#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?location ?type ?name ?resourceType ?vcpu ?memory
WHERE {
  ?component a ?type .
  ?type rdfs:subClassOf* :PhysicalInfrastructureLayer .
  ?component :name ?name .
  
  OPTIONAL { ?component :location ?location }
  OPTIONAL { ?component :resource_type ?resourceType }
  OPTIONAL { ?component :vcpu_count ?vcpu }
  OPTIONAL { ?component :cpu_count ?vcpu }
  OPTIONAL { ?component :memory_gb ?memory }
}
ORDER BY ?location ?name
"""

df_infra = query_to_dataframe(g, query_infrastructure)
print(f"Found {len(df_infra)} infrastructure components:")
df_infra

# ============================================================================
# CELL 7: Query 3 - Application Dependencies
# ============================================================================

query_dependencies = """
PREFIX : <http://example.org/it-infrastructure-ontology#>
PREFIX inst: <http://example.org/instances#>

SELECT ?app ?appName ?dependency ?depName ?relType
WHERE {
  ?app a :Application ;
       :name ?appName .
  
  {
    ?app :uses ?dependency .
    BIND("uses" AS ?relType)
  } UNION {
    ?app :calls ?dependency .
    BIND("calls" AS ?relType)
  } UNION {
    ?app :deployed_as ?dependency .
    BIND("deployed_as" AS ?relType)
  }
  
  ?dependency :name ?depName .
}
ORDER BY ?appName ?relType
"""

df_deps = query_to_dataframe(g, query_dependencies)
print(f"Found {len(df_deps)} dependencies:")
df_deps.head(20)

# ============================================================================
# CELL 8: Visualization 1 - Applications by Type
# ============================================================================

# Count applications by type
app_types = df_apps['type'].value_counts()

# Create pie chart
fig = px.pie(values=app_types.values, names=app_types.index,
             title='Applications by Type',
             color_discrete_sequence=px.colors.qualitative.Set3)
fig.update_traces(textposition='inside', textinfo='percent+label')
fig.show()

# ============================================================================
# CELL 9: Visualization 2 - Infrastructure by Location
# ============================================================================

# Count infrastructure by location
location_counts = df_infra['location'].value_counts()

# Create bar chart
fig = px.bar(x=location_counts.index, y=location_counts.values,
             title='Infrastructure Components by Location',
             labels={'x': 'Location', 'y': 'Count'},
             color=location_counts.values,
             color_continuous_scale='Viridis')
fig.update_layout(showlegend=False, xaxis_tickangle=-45)
fig.show()

# ============================================================================
# CELL 10: Visualization 3 - Resource Distribution
# ============================================================================

# Calculate total resources by location
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
    xaxis_tickangle=-45
)
fig.show()

# ============================================================================
# CELL 11: Visualization 4 - Dependency Network Graph
# ============================================================================

# Prepare data for network visualization
network_data = []
for _, row in df_deps.head(50).iterrows():  # Limit to 50 for readability
    source = get_entity_name(row['app'])
    target = get_entity_name(row['dependency'])
    label = row['relType']
    network_data.append((source, target, label))

# Create interactive network
net = visualize_network(network_data, 
                       title="Application Dependencies Network",
                       notebook=True)
net.show("dependency_network.html")
print("✓ Network visualization saved to dependency_network.html")

# ============================================================================
# CELL 12: Query 4 - Full Stack Decomposition
# ============================================================================

query_full_stack = """
PREFIX : <http://example.org/it-infrastructure-ontology#>
PREFIX inst: <http://example.org/instances#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?business ?app ?container ?infrastructure
WHERE {
  # Business Process
  ?bp a :BusinessProcess ;
      :name ?business ;
      :realized_by ?application .
  
  # Application
  ?application :name ?app .
  
  # Container (optional - legacy apps skip this)
  OPTIONAL {
    ?application :deployed_as ?pod .
    ?pod :name ?container .
  }
  
  # Infrastructure
  OPTIONAL {
    {
      ?application :runs_on ?infra .
    } UNION {
      ?pod :runs_on ?infra .
    }
    ?infra :name ?infrastructure .
  }
}
ORDER BY ?business ?app
"""

df_stack = query_to_dataframe(g, query_full_stack)
print(f"Full stack decomposition ({len(df_stack)} paths):")
df_stack

# ============================================================================
# CELL 13: Query 5 - Layer 4 Only (Physical Infrastructure)
# ============================================================================

query_layer4 = """
PREFIX : <http://example.org/it-infrastructure-ontology#>
PREFIX inst: <http://example.org/instances#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?entity ?type ?name ?location ?status
WHERE {
  ?entity a ?type .
  ?type rdfs:subClassOf* :PhysicalInfrastructureLayer .
  ?entity :name ?name .
  
  OPTIONAL { ?entity :location ?location }
  OPTIONAL { ?entity :lifecycle_status ?status }
}
ORDER BY ?type ?name
"""

df_layer4 = query_to_dataframe(g, query_layer4)
print(f"Layer 4 components ({len(df_layer4)} total):")
df_layer4

# ============================================================================
# CELL 14: Visualization 5 - Layer 4 Network
# ============================================================================

# Get Layer 4 relationships
query_layer4_rels = """
PREFIX : <http://example.org/it-infrastructure-ontology#>
PREFIX inst: <http://example.org/instances#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?source ?sourceName ?target ?targetName ?relType
WHERE {
  ?source a ?sourceType .
  ?sourceType rdfs:subClassOf* :PhysicalInfrastructureLayer .
  ?source :name ?sourceName .
  
  ?source ?rel ?target .
  ?target a ?targetType .
  ?targetType rdfs:subClassOf* :PhysicalInfrastructureLayer .
  ?target :name ?targetName .
  
  FILTER(?rel IN (:runs_on, :hosted_on, :allocated_from, :part_of))
  
  BIND(REPLACE(STR(?rel), ".*#", "") AS ?relType)
}
"""

df_layer4_rels = query_to_dataframe(g, query_layer4_rels)

# Prepare network data
layer4_network = []
for _, row in df_layer4_rels.iterrows():
    layer4_network.append((row['sourceName'], row['targetName'], row['relType']))

# Create network visualization
net_layer4 = visualize_network(layer4_network,
                               title="Physical Infrastructure Network",
                               notebook=True)
net_layer4.show("layer4_network.html")
print("✓ Layer 4 network saved to layer4_network.html")

# ============================================================================
# CELL 15: Statistics Summary
# ============================================================================

print("="*60)
print("ONTOLOGY STATISTICS SUMMARY")
print("="*60)

# Count by layer
layers = {
    "Business Processes": "BusinessProcessLayer",
    "Applications": "ApplicationLayer",
    "Containers": "ContainerLayer",
    "Infrastructure": "PhysicalInfrastructureLayer",
    "Network": "NetworkLayer",
    "Security": "SecurityLayer"
}

for layer_name, layer_class in layers.items():
    query = f"""
    PREFIX : <http://example.org/it-infrastructure-ontology#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    SELECT (COUNT(DISTINCT ?entity) AS ?count)
    WHERE {{
      ?entity a ?type .
      ?type rdfs:subClassOf* :{layer_class} .
    }}
    """
    result = list(g.query(query))
    count = int(result[0][0]) if result else 0
    print(f"{layer_name:20s}: {count:3d} entities")

print("="*60)

# Application statistics
print(f"\nApplications by Type:")
for app_type, count in app_types.items():
    print(f"  {app_type:20s}: {count}")

print(f"\nInfrastructure by Location:")
for location, count in location_counts.items():
    location_short = location.split('/')[-1][:30]
    print(f"  {location_short:30s}: {count}")

print("\n" + "="*60)

# ============================================================================
# CELL 16: Export Results
# ============================================================================

# Export to Excel
with pd.ExcelWriter('ontology_analysis_results.xlsx') as writer:
    df_apps.to_excel(writer, sheet_name='Applications', index=False)
    df_infra.to_excel(writer, sheet_name='Infrastructure', index=False)
    df_deps.to_excel(writer, sheet_name='Dependencies', index=False)
    df_stack.to_excel(writer, sheet_name='Full Stack', index=False)
    df_layer4.to_excel(writer, sheet_name='Layer 4', index=False)

print("✓ Results exported to ontology_analysis_results.xlsx")

# Export to CSV
df_apps.to_csv('applications.csv', index=False)
df_infra.to_csv('infrastructure.csv', index=False)
df_deps.to_csv('dependencies.csv', index=False)

print("✓ CSV files created")
print("  - applications.csv")
print("  - infrastructure.csv")
print("  - dependencies.csv")
