# Technology Stack

## Core Technologies

### Ontology Languages
- **OWL 2** (Web Ontology Language) - Formal ontology specification
- **RDF** (Resource Description Framework) - Data model
- **RDFS** (RDF Schema) - Basic vocabulary
- **Turtle** (.ttl) - Human-readable RDF serialization format
- **SHACL** (Shapes Constraint Language) - Validation rules

### Python Stack
- **rdflib** (>=7.0.0) - RDF graph manipulation and SPARQL queries
- **pyshacl** (>=0.25.0) - SHACL validation engine
- Python 3.x for validation and testing scripts

### Query Languages
- **SPARQL 1.1** - RDF query language for semantic databases
- **Cypher** - Property graph query language for Neo4j

## File Organization

### Ontology Files (`ontology/`)
- `it-infrastructure-ontology.ttl` - Main OWL ontology (classes, properties, relationships)
- `data-properties.ttl` - Data property definitions
- `shacl-shapes.ttl` - SHACL validation shapes
- `sample-data-*.ttl` - Instance data for different deployment scenarios

### Layer Specifications (`layer-specifications/`)
- Markdown files documenting each of the six layers
- Entity type definitions with attributes and relationships
- Framework source attributions

### Framework Analysis (`framework-analysis/`)
- Analysis documents mapping industry frameworks to ontology concepts
- TOGAF, CIM, ITIL, ArchiMate, Kubernetes, cloud provider mappings

## Common Commands

### Git Operations
```bash
# Git commands require starting a bash shell first
bash

# Then use git normally
git status
git add .
git commit -m "message"
git push
```

### Validation
```bash
# Validate sample data against SHACL shapes
python ontology/validate_sample_data.py

# Validate specific file
pyshacl -s ontology/shacl-shapes.ttl -d ontology/sample-data-cloud.ttl
```

### Testing
```bash
# Run SPARQL query tests
python ontology/test_queries.py
```

### Dependencies
```bash
# Install Python dependencies
pip install -r ontology/requirements.txt
```

## Conventions

### Naming
- Ontology namespace: `http://example.org/it-infrastructure-ontology#`
- Instance namespace: `http://example.org/instances#`
- Use PascalCase for classes (e.g., `BusinessProcess`, `VirtualMachine`)
- Use snake_case for properties (e.g., `lifecycle_status`, `runs_on`)

### File Formats
- All ontology files use Turtle (.ttl) format
- Documentation in Markdown (.md)
- Python scripts for validation and testing

### Documentation Style
- Use EARS (Easy Approach to Requirements Syntax) for requirements
- Include framework sources for all attributes
- Provide both SPARQL and Cypher query examples
- Include sample output for all query patterns
