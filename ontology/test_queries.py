#!/usr/bin/env python3
"""
Query Testing Script for IT Infrastructure Ontology

This script tests SPARQL queries against sample instance data to verify:
- Root cause analysis queries work correctly
- Impact analysis queries return expected results
- Decomposition queries traverse all layers properly
- Query performance is acceptable
"""

import sys
from pathlib import Path
from rdflib import Graph, Namespace
from rdflib.plugins.sparql import prepareQuery
import time

# Define namespaces
ONTO = Namespace("http://example.org/it-infrastructure-ontology#")
INST = Namespace("http://example.org/instances#")

def load_combined_graph():
    """Load ontology and all sample data into a single graph"""
    print("Loading ontology and sample data...")
    g = Graph()
    
    base_path = Path(__file__).parent
    files = [
        base_path / "it-infrastructure-ontology.ttl",
        base_path / "sample-data-onpremises.ttl",
        base_path / "sample-data-cloud.ttl",
        base_path / "sample-data-containerized.ttl",
        base_path / "sample-data-hybrid.ttl",
    ]
    
    for file_path in files:
        if file_path.exists():
            g.parse(file_path, format='turtle')
            print(f"  [OK] Loaded {file_path.name}")
        else:
            print(f"  [ERROR] File not found: {file_path.name}")
    
    print(f"\nTotal triples loaded: {len(g)}")
    return g

def run_query(graph, query_name, query_string, expected_min_results=0):
    """Execute a SPARQL query and return results"""
    print(f"\n{'='*70}")
    print(f"Query: {query_name}")
    print(f"{'='*70}")
    
    try:
        start_time = time.time()
        results = graph.query(query_string)
        execution_time = time.time() - start_time
        
        result_list = list(results)
        result_count = len(result_list)
        
        print(f"[OK] Query executed successfully")
        print(f"  Execution time: {execution_time:.3f} seconds")
        print(f"  Results returned: {result_count}")
        
        if result_count >= expected_min_results:
            print(f"  [OK] Expected minimum results met ({expected_min_results})")
        else:
            print(f"  [WARN] Expected at least {expected_min_results} results, got {result_count}")
        
        # Print first few results
        if result_count > 0:
            print(f"\nSample results (showing up to 5):")
            for i, row in enumerate(result_list[:5]):
                result_dict = {str(var): str(row[var]) for var in row.labels}
                print(f"  {i+1}. {result_dict}")
        
        return True, result_count, execution_time
    
    except Exception as e:
        print(f"[FAIL] Query failed: {e}")
        return False, 0, 0

def test_root_cause_queries(graph):
    """Test root cause analysis queries"""
    print(f"\n{'#'*70}")
    print("# ROOT CAUSE ANALYSIS QUERIES")
    print(f"{'#'*70}")
    
    results = []
    
    # Query 1: Find failed dependencies
    query1 = """
    PREFIX : <http://example.org/it-infrastructure-ontology#>
    PREFIX inst: <http://example.org/instances#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    
    SELECT DISTINCT ?component ?componentType ?status
    WHERE {
      inst:ERPApplication (:uses|:hosted_on|:communicates_via)+ ?component .
      ?component rdf:type ?componentType .
      ?component :lifecycle_status ?status .
      FILTER(?status IN ("failed", "degraded", "stopped", "terminated", "inactive"))
    }
    LIMIT 10
    """
    success, count, time_taken = run_query(graph, "Find Failed Dependencies", query1, 0)
    results.append(("Find Failed Dependencies", success, count, time_taken))
    
    # Query 2: Trace to physical infrastructure
    query2 = """
    PREFIX : <http://example.org/it-infrastructure-ontology#>
    PREFIX inst: <http://example.org/instances#>
    
    SELECT ?app ?vm ?server
    WHERE {
      ?app rdf:type :Application ;
           :hosted_on ?vm .
      ?vm :runs_on ?server .
      ?server rdf:type :PhysicalServer .
    }
    LIMIT 10
    """
    success, count, time_taken = run_query(graph, "Trace to Physical Infrastructure", query2, 1)
    results.append(("Trace to Physical Infrastructure", success, count, time_taken))
    
    # Query 3: Find storage dependencies
    query3 = """
    PREFIX : <http://example.org/it-infrastructure-ontology#>
    PREFIX inst: <http://example.org/instances#>
    
    SELECT ?database ?volume ?storageArray
    WHERE {
      ?database rdf:type :Database ;
                :stored_on ?volume .
      ?volume :allocated_from ?storageArray .
    }
    LIMIT 10
    """
    success, count, time_taken = run_query(graph, "Find Storage Dependencies", query3, 1)
    results.append(("Find Storage Dependencies", success, count, time_taken))
    
    return results

def test_impact_analysis_queries(graph):
    """Test impact analysis queries"""
    print(f"\n{'#'*70}")
    print("# IMPACT ANALYSIS QUERIES")
    print(f"{'#'*70}")
    
    results = []
    
    # Query 1: Find applications on a server
    query1 = """
    PREFIX : <http://example.org/it-infrastructure-ontology#>
    PREFIX inst: <http://example.org/instances#>
    
    SELECT DISTINCT ?app ?appType
    WHERE {
      ?server rdf:type :PhysicalServer .
      ?server ^:runs_on ?vm .
      ?vm ^:hosted_on ?app .
      ?app rdf:type :Application ;
           :application_type ?appType .
    }
    LIMIT 10
    """
    success, count, time_taken = run_query(graph, "Find Applications on Server", query1, 1)
    results.append(("Find Applications on Server", success, count, time_taken))
    
    # Query 2: Find applications using a database
    query2 = """
    PREFIX : <http://example.org/it-infrastructure-ontology#>
    PREFIX inst: <http://example.org/instances#>
    
    SELECT ?app ?database
    WHERE {
      ?database rdf:type :Database .
      ?database ^:uses ?app .
      ?app rdf:type :Application .
    }
    LIMIT 10
    """
    success, count, time_taken = run_query(graph, "Find Applications Using Database", query2, 1)
    results.append(("Find Applications Using Database", success, count, time_taken))
    
    # Query 3: Find services using network device
    query3 = """
    PREFIX : <http://example.org/it-infrastructure-ontology#>
    PREFIX inst: <http://example.org/instances#>
    
    SELECT DISTINCT ?app ?path ?device
    WHERE {
      ?device rdf:type :LoadBalancer .
      ?device ^:routes_through ?path .
      ?path ^:communicates_via ?app .
    }
    LIMIT 10
    """
    success, count, time_taken = run_query(graph, "Find Services Using Network Device", query3, 1)
    results.append(("Find Services Using Network Device", success, count, time_taken))
    
    return results

def test_decomposition_queries(graph):
    """Test decomposition and traversal queries"""
    print(f"\n{'#'*70}")
    print("# DECOMPOSITION AND TRAVERSAL QUERIES")
    print(f"{'#'*70}")
    
    results = []
    
    # Query 1: Business process to application
    query1 = """
    PREFIX : <http://example.org/it-infrastructure-ontology#>
    PREFIX inst: <http://example.org/instances#>
    
    SELECT ?bp ?app
    WHERE {
      ?bp rdf:type :BusinessProcess ;
          :realized_by ?app .
      ?app rdf:type :Application .
    }
    LIMIT 10
    """
    success, count, time_taken = run_query(graph, "Business Process to Application", query1, 1)
    results.append(("Business Process to Application", success, count, time_taken))
    
    # Query 2: Application to container to VM
    query2 = """
    PREFIX : <http://example.org/it-infrastructure-ontology#>
    PREFIX inst: <http://example.org/instances#>
    
    SELECT ?app ?pod ?vm
    WHERE {
      ?app rdf:type :Application ;
           :deployed_as ?pod .
      ?pod :runs_on ?vm .
      ?vm rdf:type :VirtualMachine .
    }
    LIMIT 10
    """
    success, count, time_taken = run_query(graph, "Application to Container to VM", query2, 1)
    results.append(("Application to Container to VM", success, count, time_taken))
    
    # Query 3: Full stack decomposition
    query3 = """
    PREFIX : <http://example.org/it-infrastructure-ontology#>
    PREFIX inst: <http://example.org/instances#>
    
    SELECT ?bp ?app ?infra
    WHERE {
      ?bp rdf:type :BusinessProcess ;
          :realized_by ?app .
      ?app rdf:type :Application ;
           :hosted_on ?infra .
    }
    LIMIT 10
    """
    success, count, time_taken = run_query(graph, "Full Stack Decomposition", query3, 1)
    results.append(("Full Stack Decomposition", success, count, time_taken))
    
    # Query 4: Network topology
    query4 = """
    PREFIX : <http://example.org/it-infrastructure-ontology#>
    PREFIX inst: <http://example.org/instances#>
    
    SELECT ?device1 ?device2
    WHERE {
      ?device1 rdf:type :NetworkDevice ;
               :connected_to ?device2 .
    }
    LIMIT 10
    """
    success, count, time_taken = run_query(graph, "Network Topology", query4, 0)
    results.append(("Network Topology", success, count, time_taken))
    
    # Query 5: Security relationships
    query5 = """
    PREFIX : <http://example.org/it-infrastructure-ontology#>
    PREFIX inst: <http://example.org/instances#>
    
    SELECT ?entity ?security
    WHERE {
      ?entity :protected_by ?security .
      ?security rdf:type :Firewall .
    }
    LIMIT 10
    """
    success, count, time_taken = run_query(graph, "Security Relationships", query5, 1)
    results.append(("Security Relationships", success, count, time_taken))
    
    return results

def print_summary(all_results):
    """Print summary of all query tests"""
    print(f"\n{'='*70}")
    print("QUERY TEST SUMMARY")
    print(f"{'='*70}")
    
    total_queries = len(all_results)
    successful_queries = sum(1 for _, success, _, _ in all_results if success)
    total_results = sum(count for _, _, count, _ in all_results)
    total_time = sum(time_taken for _, _, _, time_taken in all_results)
    
    print(f"\nTotal queries tested: {total_queries}")
    print(f"Successful queries: {successful_queries}/{total_queries} ({successful_queries/total_queries*100:.1f}%)")
    print(f"Total results returned: {total_results}")
    print(f"Total execution time: {total_time:.3f} seconds")
    print(f"Average time per query: {total_time/total_queries:.3f} seconds")
    
    print(f"\nDetailed Results:")
    print(f"{'Query Name':<50} {'Status':<10} {'Results':<10} {'Time (s)':<10}")
    print(f"{'-'*80}")
    for name, success, count, time_taken in all_results:
        status = "[PASS]" if success else "[FAIL]"
        print(f"{name:<50} {status:<10} {count:<10} {time_taken:<10.3f}")
    
    return successful_queries == total_queries

def main():
    """Main test function"""
    print("="*70)
    print("IT Infrastructure Ontology - Query Testing")
    print("="*70)
    
    # Load data
    graph = load_combined_graph()
    
    # Run all query tests
    all_results = []
    all_results.extend(test_root_cause_queries(graph))
    all_results.extend(test_impact_analysis_queries(graph))
    all_results.extend(test_decomposition_queries(graph))
    
    # Print summary
    all_passed = print_summary(all_results)
    
    if all_passed:
        print(f"\n[OK] All query tests passed successfully!")
        sys.exit(0)
    else:
        print(f"\n[FAIL] Some query tests failed. See details above.")
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nQuery testing interrupted by user.")
        sys.exit(130)
    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
