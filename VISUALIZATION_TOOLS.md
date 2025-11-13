# Web-Based Visualization Tools for TTL/RDF Files

## Quick Recommendations

### 🌟 Best for Quick Visualization (WORKING!)
**RDF Grapher** - http://www.ldf.fi/service/rdf-grapher
- Paste TTL content or upload file
- Interactive node-graph visualization
- Click to explore relationships
- **No installation, works immediately!**

### 🌟 Best for Interactive Exploration (WORKING!)
**RDF Gravity** - https://github.com/semweb/rdf-gravity (Download) or use online alternatives
**Better Alternative: Ontology Visualizer** - https://service.tib.eu/webvowl/
- Alternative WebVOWL instance that works
- Interactive graph visualization
- Best for ontology structure

### 🌟 Best for Professional Use (WORKING!)
**Protégé Web** - https://webprotege.stanford.edu/
- Create account (free)
- Upload ontology
- Professional ontology editor with visualization
- Collaborative features

### 🌟 NEW: Best for Modern Visualization (WORKING!)
**RDF Shape** - https://rdfshape.weso.es/
- Multiple visualization options
- SHACL validation
- SPARQL queries
- Modern interface

---

## Detailed Tool Comparison

### 1. RDF Shape (Recommended - Modern & Working!)

**URL**: https://rdfshape.weso.es/

**Features**:
- Multiple visualization modes
- SHACL validation built-in
- SPARQL query interface
- Modern, responsive interface
- Export options
- No registration required

**How to Use**:
1. Go to https://rdfshape.weso.es/
2. Click "Data" tab
3. Paste your TTL content or upload file
4. Click "Visualize" tab
5. Choose visualization type (Graph, Tree, etc.)
6. Explore interactively

**Best For**:
- Modern, reliable visualization
- Combined validation and visualization
- Understanding both structure and data
- SPARQL queries on your data

**Limitations**:
- May need to adjust for very large files

---

### 2. RDF Grapher

**URL**: http://www.ldf.fi/service/rdf-grapher

**Features**:
- Simple paste-and-visualize interface
- Interactive graph with clickable nodes
- Shows both classes and instances
- Color-coded by type
- Export options

**How to Use**:
1. Go to http://www.ldf.fi/service/rdf-grapher
2. Paste your TTL content or upload file
3. Click "Visualize"
4. Click nodes to explore relationships

**Best For**:
- Exploring instance data
- Understanding relationships between entities
- Quick visualization without setup

**Limitations**:
- Can be overwhelming with large datasets
- Limited layout control

---

### 3. LodLive

**URL**: http://en.lodlive.it/

**Features**:
- Interactive exploration starting from a URI
- Expands graph as you click
- Shows incoming and outgoing relationships
- Clean, modern interface

**How to Use**:
1. Go to http://en.lodlive.it/
2. Upload your TTL file or provide SPARQL endpoint
3. Enter a starting URI
4. Click to expand and explore

**Best For**:
- Exploring specific entities and their connections
- Understanding dependency chains
- Interactive discovery

**Limitations**:
- Requires starting URI
- Better for exploration than overview

---

### 4. Protégé Web

**URL**: https://webprotege.stanford.edu/

**Features**:
- Full-featured ontology editor
- Multiple visualization plugins
- Class hierarchy browser
- Individuals browser
- SPARQL query interface
- Collaborative editing
- Version control

**How to Use**:
1. Create free account at https://webprotege.stanford.edu/
2. Create new project
3. Upload your TTL file
4. Use "Class hierarchy" tab for structure
5. Use "Individuals" tab for instances
6. Install visualization plugins (OntoGraf, etc.)

**Best For**:
- Professional ontology development
- Team collaboration
- Comprehensive analysis
- Long-term projects

**Limitations**:
- Requires account creation
- More complex interface
- Steeper learning curve

---

### 5. RDF Translator + GraphViz

**URL**: http://rdf-translator.appspot.com/

**Features**:
- Convert TTL to various formats
- Generate DOT format for GraphViz
- Can visualize with online GraphViz tools

**How to Use**:
1. Go to http://rdf-translator.appspot.com/
2. Paste TTL content
3. Convert to "GraphViz DOT"
4. Copy output
5. Go to http://viz-js.com/ or https://dreampuf.github.io/GraphvizOnline/
6. Paste DOT content and visualize

**Best For**:
- Creating static diagrams
- Export for documentation
- Custom styling with DOT language

**Limitations**:
- Two-step process
- Less interactive
- Manual layout adjustments needed

---

### 6. TIB WebVOWL (Working Alternative to Original WebVOWL)

**URL**: https://service.tib.eu/webvowl/

**Features**:
- Specialized OWL visualization
- Clear visual notation
- Multiple layout algorithms
- Export capabilities
- **This is a working instance of WebVOWL!**

**How to Use**:
1. Go to https://service.tib.eu/webvowl/
2. Click "Ontology" → "Select ontology file"
3. Upload `it-infrastructure-ontology.ttl`
4. Choose layout algorithm
5. Customize visualization
6. Export as needed

**Best For**:
- Academic presentations
- Ontology documentation
- Understanding OWL constructs
- Class hierarchy visualization

---

### 7. Gruff (Franz AllegroGraph)

**URL**: https://allegrograph.com/products/gruff/

**Features**:
- Professional RDF browser
- Advanced visualization
- SPARQL query builder
- Free for small datasets

**How to Use**:
1. Download Gruff (free version available)
2. Load TTL file
3. Explore with visual query builder
4. Generate custom views

**Best For**:
- Professional analysis
- Complex queries
- Large datasets

**Limitations**:
- Requires download (not purely web-based)
- Free version has limitations

---

### 8. GraphDB Workbench (Excellent Free Option)

**URL**: https://www.ontotext.com/products/graphdb/graphdb-free/

**Features**:
- Professional RDF database with visualization
- Visual graph explorer
- SPARQL query interface
- Import/export capabilities
- Free version available

**How to Use**:
1. Download GraphDB Free (or use cloud trial)
2. Install and start GraphDB
3. Create repository
4. Import your TTL files
5. Use "Explore" → "Visual Graph" for visualization
6. Query with SPARQL

**Best For**:
- Professional-grade visualization
- Large datasets
- Complex queries
- Long-term projects

**Limitations**:
- Requires download and installation
- Not purely web-based

---

### 9. Ontology Lookup Service (OLS)

**URL**: https://www.ebi.ac.uk/ols/index

**Features**:
- Browse ontologies online
- Tree and graph views
- Search functionality
- REST API

**How to Use**:
1. Upload ontology to OLS (requires submission)
2. Or use for reference/comparison
3. Browse with tree view
4. Explore relationships

**Best For**:
- Public ontologies
- Reference and comparison
- Academic use

**Limitations**:
- Requires ontology submission for custom ontologies
- Better for browsing than editing

---

### 10. LODE (Live OWL Documentation Environment)

**URL**: https://essepuntato.it/lode/

**Features**:
- Generates HTML documentation from OWL
- Includes visual diagrams
- Professional documentation format
- No installation needed

**How to Use**:
1. Go to https://essepuntato.it/lode/
2. Provide URL to your TTL file (or use local server)
3. Generate documentation
4. View classes, properties, and relationships

**Best For**:
- Creating documentation
- Sharing ontology with stakeholders
- Professional presentations

**Limitations**:
- Requires accessible URL (not for local files directly)
- Static documentation rather than interactive

---

## Recommended Workflow for Your Architecture

### Step 1: Quick Visualization (Start Here!)
Use **RDF Shape** for immediate results:
```
https://rdfshape.weso.es/
1. Click "Data" tab
2. Upload: ontology/sample-data-complex-hybrid.ttl
3. Click "Visualize" tab
4. Explore your architecture!
```

### Step 2: Explore Instance Data
Use **RDF Grapher** to see your complex architecture:
```
http://www.ldf.fi/service/rdf-grapher
Upload: ontology/sample-data-complex-hybrid.ttl
Click "Visualize"
```

### Step 3: Visualize Ontology Structure
Use **TIB WebVOWL** (working alternative) to understand the class hierarchy:
```
https://service.tib.eu/webvowl/
Upload: ontology/it-infrastructure-ontology.ttl
Explore class relationships
```

### Step 4: Professional Analysis (Optional)
Use **Protégé Web** for detailed exploration:
```
https://webprotege.stanford.edu/
Create project and upload files
Use multiple views for comprehensive analysis
```

---

## Quick Start: Visualize Your Complex Architecture

### Option A: Fastest (RDF Grapher)

1. Open http://www.ldf.fi/service/rdf-grapher
2. Click "Choose File"
3. Select `ontology/sample-data-complex-hybrid.ttl`
4. Click "Visualize"
5. Explore the interactive graph!

### Option B: Best Quality (RDF Shape - Modern!)

1. Open https://rdfshape.weso.es/
2. Click "Data" tab
3. Upload `ontology/sample-data-complex-hybrid.ttl`
4. Click "Visualize" tab
5. Choose visualization type
6. Explore interactively!

### Option B-Alt: Ontology Structure (TIB WebVOWL)

1. Open https://service.tib.eu/webvowl/
2. Click "Ontology" → "Select ontology file"
3. Select `ontology/it-infrastructure-ontology.ttl`
4. Explore the class structure
5. Export as SVG for documentation

### Option C: Most Features (Protégé Web)

1. Go to https://webprotege.stanford.edu/
2. Sign up (free)
3. Create new project: "IT Infrastructure Ontology"
4. Upload `it-infrastructure-ontology.ttl`
5. Upload `sample-data-complex-hybrid.ttl`
6. Use tabs to explore:
   - Classes: See entity types
   - Individuals: See instances
   - OntoGraf: Visual graph

---

## Tips for Better Visualization

### 1. Filter Large Datasets
If visualization is slow, create filtered versions:

```bash
# Extract only applications and databases
grep -A 5 "a :Application\|a :Database" sample-data-complex-hybrid.ttl > filtered.ttl
```

### 2. Use SPARQL to Create Subgraphs

Create focused views with SPARQL:

```sparql
# Extract only Azure components
CONSTRUCT {
  ?s ?p ?o
}
WHERE {
  ?s ?p ?o .
  FILTER(CONTAINS(STR(?s), "Azure") || CONTAINS(STR(?o), "Azure"))
}
```

### 3. Combine with Mermaid Diagrams

For documentation, use the Mermaid diagrams in `VISUAL_DIAGRAMS.md`:
- Render in GitHub
- Use Mermaid Live Editor: https://mermaid.live/
- Export as PNG/SVG

### 4. Use Neo4j for Interactive Exploration

Load into Neo4j for powerful visualization:

```bash
# Install Neo4j Desktop (free)
# Use neosemantics plugin to import RDF
# Use Neo4j Browser for interactive exploration
```

---

## Comparison Table

| Tool | Setup | Best For | Interactive | Export | Free | Status |
|------|-------|----------|-------------|--------|------|--------|
| **RDF Shape** | None | Modern visualization | Yes | Yes | Yes | ✅ Working |
| **RDF Grapher** | None | Instance data | Yes | Limited | Yes | ✅ Working |
| **TIB WebVOWL** | None | Ontology structure | Yes | SVG/PNG | Yes | ✅ Working |
| **Protégé Web** | Account | Professional use | Yes | Yes | Yes | ✅ Working |
| **GraphDB** | Download | Advanced analysis | Yes | Yes | Yes (Free) | ✅ Working |
| LodLive | None | Exploration | Yes | No | Yes | ⚠️ May vary |
| RDF Translator | None | Static diagrams | No | DOT | Yes | ✅ Working |
| Original WebVOWL | None | Ontology structure | Yes | SVG/PNG | Yes | ❌ Not working |

---

## Troubleshooting

### File Too Large
- Split into smaller files by layer
- Use SPARQL to extract subsets
- Filter to specific entity types

### Visualization Slow
- Use WebVOWL for ontology only (no instances)
- Use RDF Grapher with filtered data
- Consider local tools (Protégé Desktop)

### Can't See Relationships
- Ensure inverse properties are defined
- Check that relationships use correct URIs
- Verify namespace prefixes

### Export Quality Issues
- Use SVG format for scalability
- Adjust zoom level before export
- Use GraphViz for publication-quality diagrams

---

## Additional Resources

### Online SPARQL Endpoints
If you want to query and visualize:
- **Yasgui**: https://yasgui.triply.cc/
- **SPARQL Playground**: https://sparql-playground.sib.swiss/

### RDF Validators
Before visualizing, validate your TTL:
- **RDF Validator**: http://www.w3.org/RDF/Validator/
- **TTL Validator**: http://ttl.summerofcode.be/

### Learning Resources
- **WebVOWL Tutorial**: http://vowl.visualdataweb.org/webvowl/
- **Protégé Tutorial**: https://protegewiki.stanford.edu/wiki/WebProtegeUsersGuide

---

## ✅ Recommended: Start Here! (Updated - All Working!)

For your complex hybrid architecture, I recommend this order:

### 1. **First**: Try RDF Shape (https://rdfshape.weso.es/) ⭐ BEST CHOICE
   - Modern, reliable, feature-rich
   - Upload `sample-data-complex-hybrid.ttl`
   - Multiple visualization options
   - Built-in SHACL validation
   - SPARQL query interface
   - **This is your best bet for immediate results!**

### 2. **Alternative**: Try RDF Grapher (http://www.ldf.fi/service/rdf-grapher)
   - Simple and fast
   - Upload `sample-data-complex-hybrid.ttl`
   - Get immediate visual feedback
   - Explore relationships interactively
   - Good backup if RDF Shape is slow

### 3. **For Ontology Structure**: Try TIB WebVOWL (https://service.tib.eu/webvowl/)
   - Working alternative to original WebVOWL
   - Upload `it-infrastructure-ontology.ttl`
   - Understand the class hierarchy
   - Export diagrams for documentation
   - Professional-looking visualizations

### 4. **For Long-term**: Consider Protégé Web (https://webprotege.stanford.edu/)
   - Professional features
   - Team collaboration
   - Long-term project management
   - Multiple visualization plugins

### 5. **For Advanced Use**: Download GraphDB Free
   - Most powerful option
   - Professional-grade visualization
   - Excellent for large datasets
   - SPARQL query interface
   - Worth the download for serious work

---

**Last Updated**: 2024-01-15  
**Status**: Complete

