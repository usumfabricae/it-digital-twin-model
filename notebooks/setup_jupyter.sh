#!/bin/bash
# Setup script for Jupyter notebook analysis

echo "=========================================="
echo "Jupyter Notebook Setup"
echo "=========================================="

# Install required packages
echo ""
echo "Installing required packages..."
pip install rdflib pandas matplotlib networkx pyvis plotly openpyxl jupyter

# Check if installation was successful
if [ $? -eq 0 ]; then
    echo "✓ Packages installed successfully"
else
    echo "✗ Installation failed"
    exit 1
fi

# Start Jupyter
echo ""
echo "=========================================="
echo "Starting Jupyter Notebook..."
echo "=========================================="
echo ""
echo "Instructions:"
echo "1. Create a new notebook in the notebooks/ directory"
echo "2. Copy cells from ontology_visualization.py"
echo "3. Run cells sequentially"
echo ""
echo "Press Ctrl+C to stop Jupyter when done"
echo ""

jupyter notebook
