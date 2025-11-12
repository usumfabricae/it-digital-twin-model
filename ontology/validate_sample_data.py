#!/usr/bin/env python3
"""
SHACL Validation Script for IT Infrastructure Ontology Sample Data

This script validates sample instance data against SHACL shapes to ensure:
- Mandatory attributes are present
- Enumeration values are valid
- Relationship cardinality constraints are met
- Cross-layer relationship rules are followed
"""

import sys
from pathlib import Path
from rdflib import Graph
from pyshacl import validate

def load_graph(file_path):
    """Load RDF graph from file"""
    g = Graph()
    try:
        g.parse(file_path, format='turtle')
        print(f"✓ Loaded {len(g)} triples from {file_path}")
        return g
    except Exception as e:
        print(f"✗ Error loading {file_path}: {e}")
        return None

def validate_data(data_graph, shapes_graph, ontology_graph, scenario_name):
    """Validate data graph against SHACL shapes"""
    print(f"\n{'='*70}")
    print(f"Validating: {scenario_name}")
    print(f"{'='*70}")
    
    # Combine ontology and data for validation
    combined_graph = data_graph + ontology_graph
    
    # Run SHACL validation
    conforms, results_graph, results_text = validate(
        combined_graph,
        shacl_graph=shapes_graph,
        ont_graph=ontology_graph,
        inference='rdfs',
        abort_on_first=False,
        allow_warnings=True,
        meta_shacl=False,
        advanced=True,
        js=False
    )
    
    # Print results
    if conforms:
        print(f"✓ VALIDATION PASSED: All constraints satisfied")
        print(f"  - {len(data_graph)} triples validated successfully")
        return True, []
    else:
        print(f"✗ VALIDATION FAILED: Constraint violations found")
        print(f"\nValidation Report:")
        print(results_text)
        
        # Parse violations for structured output
        violations = []
        for line in results_text.split('\n'):
            if 'Validation Result' in line or 'Message:' in line or 'Focus Node:' in line:
                violations.append(line.strip())
        
        return False, violations

def main():
    """Main validation function"""
    print("="*70)
    print("IT Infrastructure Ontology - Sample Data Validation")
    print("="*70)
    
    # Define file paths
    base_path = Path(__file__).parent
    ontology_file = base_path / "it-infrastructure-ontology.ttl"
    shapes_file = base_path / "shacl-shapes.ttl"
    
    sample_files = [
        ("On-Premises Infrastructure", base_path / "sample-data-onpremises.ttl"),
        ("Cloud Infrastructure (AWS)", base_path / "sample-data-cloud.ttl"),
        ("Containerized Applications (Kubernetes/OpenShift)", base_path / "sample-data-containerized.ttl"),
        ("Hybrid Infrastructure", base_path / "sample-data-hybrid.ttl"),
    ]
    
    # Load ontology and shapes
    print("\nLoading ontology and SHACL shapes...")
    ontology_graph = load_graph(ontology_file)
    shapes_graph = load_graph(shapes_file)
    
    if not ontology_graph or not shapes_graph:
        print("\n✗ Failed to load ontology or shapes. Exiting.")
        sys.exit(1)
    
    # Validate each sample data file
    results = {}
    all_violations = []
    
    for scenario_name, sample_file in sample_files:
        if not sample_file.exists():
            print(f"\n✗ Sample file not found: {sample_file}")
            results[scenario_name] = False
            continue
        
        data_graph = load_graph(sample_file)
        if not data_graph:
            results[scenario_name] = False
            continue
        
        conforms, violations = validate_data(data_graph, shapes_graph, ontology_graph, scenario_name)
        results[scenario_name] = conforms
        
        if violations:
            all_violations.extend([(scenario_name, v) for v in violations])
    
    # Print summary
    print(f"\n{'='*70}")
    print("VALIDATION SUMMARY")
    print(f"{'='*70}")
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for scenario, passed_validation in results.items():
        status = "✓ PASS" if passed_validation else "✗ FAIL"
        print(f"{status}: {scenario}")
    
    print(f"\nTotal: {passed}/{total} scenarios passed validation")
    
    if all_violations:
        print(f"\n{'='*70}")
        print("DETAILED VIOLATIONS")
        print(f"{'='*70}")
        for scenario, violation in all_violations:
            print(f"\n[{scenario}]")
            print(f"  {violation}")
    
    # Exit with appropriate code
    if passed == total:
        print(f"\n✓ All validations passed successfully!")
        sys.exit(0)
    else:
        print(f"\n✗ {total - passed} validation(s) failed. See details above.")
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nValidation interrupted by user.")
        sys.exit(130)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
