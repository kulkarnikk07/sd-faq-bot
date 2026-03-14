"""
San Diego FAQ Bot - Data Loader
Loads and processes CSV data from San Diego Open Data Portal
and PDF documents for RAG-based question answering
"""

import pandas as pd
import os
from pathlib import Path
import PyPDF2
from typing import Dict, List, Optional
import json


class SanDiegoDataLoader:
    """Handles loading and processing of all data sources"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.permits_data = None
        self.neighborhoods_data = None
        self.zoning_data = None
        self.pdf_content = None
        
    def load_all_data(self):
        """Load all available data sources"""
        print("Loading San Diego data...")
        
        # Load CSV data
        self.load_permits()
        self.load_neighborhoods()
        self.load_zoning()
        
        # Load PDF if it exists
        self.load_pdf_documents()
        
        print("✅ All data loaded successfully!")
        return self
    
    def load_permits(self):
        """Load development permit data"""
        permits_dir = self.data_dir / "permits"
        
        if not permits_dir.exists():
            print("⚠️  Permits directory not found, skipping...")
            return
        
        data = {}
        
        # Load active permits
        active_file = permits_dir / "active_approvals.csv"
        if active_file.exists():
            print(f"Loading active permits from {active_file}...")
            data['active'] = pd.read_csv(active_file, low_memory=False)
            print(f"  ✓ Loaded {len(data['active'])} active permits")
        
        # Load closed permits
        closed_file = permits_dir / "closed_approvals.csv"
        if closed_file.exists():
            print(f"Loading closed permits from {closed_file}...")
            data['closed'] = pd.read_csv(closed_file, low_memory=False)
            print(f"  ✓ Loaded {len(data['closed'])} closed permits")
        
        # Load permit dictionary
        dict_file = permits_dir / "permit_dictionary.csv"
        if dict_file.exists():
            print(f"Loading permit dictionary from {dict_file}...")
            data['dictionary'] = pd.read_csv(dict_file)
            print(f"  ✓ Loaded permit dictionary")
        
        # Load permit tags
        tags_file = permits_dir / "permit_tags.csv"
        if tags_file.exists():
            print(f"Loading permit tags from {tags_file}...")
            data['tags'] = pd.read_csv(tags_file, low_memory=False)
            print(f"  ✓ Loaded {len(data['tags'])} permit tags")
        
        self.permits_data = data
        return data
    
    def load_neighborhoods(self):
        """Load neighborhood and community data"""
        neighborhoods_dir = self.data_dir / "neighborhoods"
        
        if not neighborhoods_dir.exists():
            print("⚠️  Neighborhoods directory not found, skipping...")
            return
        
        data = {}
        
        # Load community planning districts
        cpd_file = neighborhoods_dir / "community_planning_districts.csv"
        if cpd_file.exists():
            print(f"Loading community planning districts from {cpd_file}...")
            data['communities'] = pd.read_csv(cpd_file)
            print(f"  ✓ Loaded {len(data['communities'])} communities")
        
        # Load council districts
        council_file = neighborhoods_dir / "council_districts.csv"
        if council_file.exists():
            print(f"Loading council districts from {council_file}...")
            data['council_districts'] = pd.read_csv(council_file)
            print(f"  ✓ Loaded {len(data['council_districts'])} council districts")
        
        # Load police neighborhoods
        police_file = neighborhoods_dir / "police_neighborhoods.csv"
        if police_file.exists():
            print(f"Loading police neighborhoods from {police_file}...")
            data['police_neighborhoods'] = pd.read_csv(police_file)
            print(f"  ✓ Loaded {len(data['police_neighborhoods'])} police neighborhoods")
        
        self.neighborhoods_data = data
        return data
    
    def load_zoning(self):
        """Load zoning data"""
        zoning_dir = self.data_dir / "zoning"
        
        if not zoning_dir.exists():
            print("⚠️  Zoning directory not found, skipping...")
            return
        
        data = {}
        
        # Load zoning designations
        zoning_file = zoning_dir / "zoning_designations.csv"
        if zoning_file.exists():
            print(f"Loading zoning designations from {zoning_file}...")
            data['designations'] = pd.read_csv(zoning_file)
            print(f"  ✓ Loaded {len(data['designations'])} zoning designations")
        
        self.zoning_data = data
        return data
    
    def load_pdf_documents(self):
        """Load PDF municipal documents"""
        documents_dir = self.data_dir.parent / "documents"
        
        if not documents_dir.exists():
            # Try current directory
            pdf_files = list(Path(".").glob("*.pdf"))
        else:
            pdf_files = list(documents_dir.glob("*.pdf"))
        
        if not pdf_files:
            print("⚠️  No PDF files found, skipping...")
            return
        
        pdf_content = {}
        
        for pdf_file in pdf_files:
            print(f"Loading PDF: {pdf_file.name}...")
            try:
                with open(pdf_file, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    text = ""
                    for page_num, page in enumerate(pdf_reader.pages):
                        text += f"\n--- Page {page_num + 1} ---\n"
                        text += page.extract_text()
                    
                    pdf_content[pdf_file.stem] = text
                    print(f"  ✓ Loaded {len(pdf_reader.pages)} pages from {pdf_file.name}")
            except Exception as e:
                print(f"  ✗ Error loading {pdf_file.name}: {e}")
        
        self.pdf_content = pdf_content
        return pdf_content
    
    def get_permit_statistics(self) -> Dict:
        """Get summary statistics about permits"""
        if not self.permits_data:
            return {}
        
        stats = {}
        
        if 'active' in self.permits_data:
            active = self.permits_data['active']
            stats['active_count'] = len(active)
            
            # Get permit types if column exists
            if 'approval_type' in active.columns:
                stats['active_by_type'] = active['approval_type'].value_counts().to_dict()
        
        if 'closed' in self.permits_data:
            closed = self.permits_data['closed']
            stats['closed_count'] = len(closed)
            
            if 'approval_type' in closed.columns:
                stats['closed_by_type'] = closed['approval_type'].value_counts().to_dict()
        
        return stats
    
    def search_permits(self, query: str, limit: int = 10) -> List[Dict]:
        """Search permits by keyword"""
        if not self.permits_data or 'active' not in self.permits_data:
            return []
        
        active = self.permits_data['active']
        
        # Search across multiple columns
        search_columns = ['approval_type', 'project_title', 'work_description']
        available_columns = [col for col in search_columns if col in active.columns]
        
        if not available_columns:
            return []
        
        # Create search mask
        mask = pd.Series([False] * len(active))
        query_lower = query.lower()
        
        for col in available_columns:
            mask |= active[col].astype(str).str.lower().str.contains(query_lower, na=False)
        
        results = active[mask].head(limit)
        return results.to_dict('records')
    
    def get_community_info(self, community_name: str) -> Optional[Dict]:
        """Get information about a specific community"""
        if not self.neighborhoods_data or 'communities' not in self.neighborhoods_data:
            return None
        
        communities = self.neighborhoods_data['communities']
        
        # Search for community (case-insensitive)
        name_column = 'cpname' if 'cpname' in communities.columns else communities.columns[0]
        
        match = communities[
            communities[name_column].str.lower() == community_name.lower()
        ]
        
        if len(match) > 0:
            return match.iloc[0].to_dict()
        
        return None
    
    def get_knowledge_base_text(self) -> str:
        """
        Get all text content for RAG/context
        This combines PDF content with structured data summaries
        """
        context_parts = []
        
        # Add PDF content
        if self.pdf_content:
            context_parts.append("=== MUNICIPAL CODE AND REGULATIONS ===\n")
            for doc_name, content in self.pdf_content.items():
                context_parts.append(f"\n--- {doc_name} ---\n")
                context_parts.append(content)
        
        # Add permit statistics
        if self.permits_data:
            context_parts.append("\n\n=== PERMIT INFORMATION ===\n")
            stats = self.get_permit_statistics()
            context_parts.append(json.dumps(stats, indent=2))
        
        # Add neighborhood information
        if self.neighborhoods_data and 'communities' in self.neighborhoods_data:
            context_parts.append("\n\n=== COMMUNITY PLANNING DISTRICTS ===\n")
            communities = self.neighborhoods_data['communities']
            
            # Get community names
            name_col = 'cpname' if 'cpname' in communities.columns else communities.columns[0]
            community_list = communities[name_col].tolist()
            context_parts.append(f"San Diego has {len(community_list)} community planning districts:\n")
            context_parts.append(", ".join(community_list[:50]))  # First 50
        
        return "\n".join(context_parts)
    
    def get_data_summary(self) -> Dict:
        """Get a summary of all loaded data"""
        summary = {
            'permits': {},
            'neighborhoods': {},
            'zoning': {},
            'documents': {}
        }
        
        if self.permits_data:
            for key, df in self.permits_data.items():
                if isinstance(df, pd.DataFrame):
                    summary['permits'][key] = {
                        'rows': len(df),
                        'columns': list(df.columns)
                    }
        
        if self.neighborhoods_data:
            for key, df in self.neighborhoods_data.items():
                if isinstance(df, pd.DataFrame):
                    summary['neighborhoods'][key] = {
                        'rows': len(df),
                        'columns': list(df.columns)
                    }
        
        if self.zoning_data:
            for key, df in self.zoning_data.items():
                if isinstance(df, pd.DataFrame):
                    summary['zoning'][key] = {
                        'rows': len(df),
                        'columns': list(df.columns)
                    }
        
        if self.pdf_content:
            summary['documents'] = {
                name: f"{len(content)} characters"
                for name, content in self.pdf_content.items()
            }
        
        return summary


# Convenience function for backwards compatibility
def load_data(data_dir: str = "data"):
    """Load all San Diego data - compatible with existing app.py"""
    loader = SanDiegoDataLoader(data_dir)
    loader.load_all_data()
    return loader


if __name__ == "__main__":
    # Test the data loader
    print("=" * 60)
    print("San Diego Data Loader Test")
    print("=" * 60)
    
    loader = load_data()
    
    print("\n" + "=" * 60)
    print("Data Summary:")
    print("=" * 60)
    
    summary = loader.get_data_summary()
    print(json.dumps(summary, indent=2))
    
    print("\n" + "=" * 60)
    print("Permit Statistics:")
    print("=" * 60)
    
    stats = loader.get_permit_statistics()
    print(json.dumps(stats, indent=2))
    
    print("\n✅ Data loader test complete!")