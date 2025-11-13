# Jupyter Notebook - Complete Package Summary

## ✅ Everything You Need is Ready!

I've created a complete Jupyter notebook solution for querying and visualizing your IT Infrastructure Ontology.

---

## 📁 Files Created

```
notebooks/
├── README.md                      # Complete guide
├── EXAMPLES.md                    # 12 copy-paste examples
├── SUMMARY.md                     # This file
├── requirements.txt               # Package dependencies
├── setup_jupyter.bat              # Windows setup script
├── setup_jupyter.sh               # Linux/Mac setup script
└── ontology_visualization.py      # All code (16 cells)
```

---

## 🚀 Quick Start (3 Commands)

### Windows
```bash
cd notebooks
pip install -r requirements.txt
jupyter notebook
```

### Linux/Mac
```bash
cd notebooks
pip install -r requirements.txt
jupyter notebook
```

---

## 📊 What You Get

### 1. Interactive Queries
- Query with SPARQL
- Results as pandas DataFrames
- Easy filtering and sorting

### 2. Beautiful Visualizations
- **Pie charts** - Application distribution
- **Bar charts** - Infrastructure by location
- **Network graphs** - Interactive dependencies
- **Heatmaps** - Resource distribution

### 3. Data Export
- Excel (multiple sheets)
- CSV files
- HTML reports
- Interactive HTML graphs

### 4. Pre-Built Queries
- List all applications
- Physical infrastructure
- Dependencies
- Full stack decomposition
- Layer 4 only

---

## 📖 Documentation

### Main Guide
**`README.md`** - Complete documentation with:
- Installation instructions
- Query examples
- Visualization examples
- Troubleshooting

### Examples
**`EXAMPLES.md`** - 12 ready-to-use examples:
1. Basic setup and query
2. Plotly visualizations
3. Infrastructure analysis
4. Resource summaries
5. Dependency networks
6. Full stack traces
7. Export to Excel/CSV
8. Interactive filtering
9. Heatmaps
10. Statistics dashboard
11. Custom query functions
12. Save/load analysis

### Code
**`ontology_visualization.py`** - Complete notebook code:
- 16 cells ready to copy
- All imports included
- Helper functions
- Queries and visualizations
- Export functionality

---

## 🎯 How to Use

### Method 1: Copy-Paste (Recommended)

1. Start Jupyter: `jupyter notebook`
2. Create new notebook
3. Open `ontology_visualization.py`
4. Copy each `# CELL X:` section
5. Paste into notebook cells
6. Run with Shift+Enter

### Method 2: Use Examples

1. Start Jupyter: `jupyter notebook`
2. Create new notebook
3. Open `EXAMPLES.md`
4. Copy any example
5. Paste and run

### Method 3: Run as Script

```python
# In Jupyter cell
%run ontology_visualization.py
```

---

## 📦 Package Requirements

All packages listed in `requirements.txt`:

```
rdflib>=6.0.0          # RDF/SPARQL
pandas>=1.3.0          # Data manipulation
matplotlib>=3.4.0      # Basic plots
plotly>=5.0.0          # Interactive plots
networkx>=2.6.0        # Network graphs
pyvis>=0.3.0           # Interactive networks
openpyxl>=3.0.0        # Excel export
jupyter>=1.0.0         # Jupyter notebook
```

Install all at once:
```bash
pip install -r requirements.txt
```

---

## 🎨 Visualization Examples

### Pie Chart
```python
fig = px.pie(values=counts, names=labels, title='Distribution')
fig.show()
```

### Bar Chart
```python
fig = px.bar(x=categories, y=values, title='Comparison')
fig.show()
```

### Network Graph
```python
net = Network(height="600px", notebook=True)
net.add_nodes(nodes)
net.add_edges(edges)
net.show("graph.html")
```

### Heatmap
```python
sns.heatmap(data, annot=True, cmap='YlOrRd')
plt.show()
```

---

## 🔍 Query Examples

### Simple Query
```python
query = """
SELECT ?name ?type WHERE {
  ?app a :Application ; :name ?name ; :application_type ?type .
}
"""
df = query_to_dataframe(g, query)
```

### Filtered Query
```python
query = """
SELECT ?name WHERE {
  ?app a :Application ; 
       :name ?name ; 
       :lifecycle_status "production" .
}
"""
```

### Aggregation Query
```python
query = """
SELECT ?location (SUM(?vcpu) AS ?total) WHERE {
  ?entity :location ?location ; :vcpu_count ?vcpu .
}
GROUP BY ?location
"""
```

---

## 💡 Pro Tips

### 1. Start Simple
Begin with basic queries, add complexity gradually

### 2. Use DataFrames
Pandas makes data manipulation easy:
```python
df.head(10)                    # First 10 rows
df[df['status'] == 'prod']     # Filter
df.groupby('type').size()      # Count by type
```

### 3. Visualize Early
Create charts to understand your data quickly

### 4. Export Results
Save your analysis:
```python
df.to_excel('results.xlsx')
df.to_csv('results.csv')
```

### 5. Document
Add markdown cells to explain your analysis

---

## 🎓 Learning Path

### Beginner
1. Run Example 1 (Basic setup)
2. Run Example 2 (Simple visualization)
3. Modify queries slightly
4. Export results

### Intermediate
1. Write custom queries
2. Create custom visualizations
3. Filter and aggregate data
4. Build dashboards

### Advanced
1. Complex SPARQL queries
2. Interactive widgets
3. Custom network layouts
4. Automated reports

---

## 📤 Output Files

Running the notebook creates:

- `dependency_network.html` - Interactive dependency graph
- `layer4_network.html` - Interactive infrastructure graph
- `ontology_analysis_results.xlsx` - All results in Excel
- `applications.csv` - Application data
- `infrastructure.csv` - Infrastructure data
- `dependencies.csv` - Dependency relationships

---

## 🆘 Troubleshooting

### Jupyter won't start
```bash
pip install --upgrade jupyter
```

### Packages not found
```bash
pip install -r requirements.txt
```

### Graph is empty
```python
# Check file path
import os
print(os.getcwd())
```

### Visualization not showing
```python
# For Plotly
import plotly.io as pio
pio.renderers.default = "notebook"
```

---

## ✨ Key Features

✅ **Interactive** - Modify and re-run instantly  
✅ **Visual** - Beautiful charts and graphs  
✅ **Exportable** - Save to Excel, CSV, HTML  
✅ **Shareable** - Share notebooks with team  
✅ **Documented** - Complete guides included  
✅ **Extensible** - Easy to customize  

---

## 🎯 Next Steps

1. ✅ Install packages: `pip install -r requirements.txt`
2. ✅ Start Jupyter: `jupyter notebook`
3. ✅ Create new notebook
4. ✅ Copy cells from `ontology_visualization.py`
5. ✅ Run and explore!
6. ✅ Customize for your needs

---

## 📚 Additional Resources

- **Main Guide**: `README.md`
- **Examples**: `EXAMPLES.md`
- **Quick Start**: `../JUPYTER_QUICK_START.md`
- **Layer 4 Guide**: `../LAYER4_VISUALIZATION_GUIDE.md`

---

## 🎉 You're Ready!

Everything is set up and ready to use. Just:

```bash
cd notebooks
pip install -r requirements.txt
jupyter notebook
```

Then start exploring your ontology data!

---

**Created**: 2024-01-15  
**Status**: ✅ Complete and ready to use  
**Support**: See README.md for detailed help

