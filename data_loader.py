"""
San Diego FAQ Bot - Data Loader
Loads and processes CSV data from San Diego Open Data Portal
and PDF documents for RAG-based question answering

Supports both local files and remote URLs for deployment flexibility
"""

import pandas as pd
import os
from pathlib import Path
import PyPDF2
from typing import Dict, List, Optional
import json


class SanDiegoDataLoader:
    """Handles loading and processing of all data sources"""
    
    # San Diego Open Data Portal URLs
    DATA_URLS = {
        'permits_active': 'https://seshat.datasd.org/dsd/dsd_approvals_set2_active.csv',
        'permits_closed': 'https://seshat.datasd.org/dsd/dsd_approvals_set2_closed.csv',
        'communities': 'https://seshat.datasd.org/sde/cmty_plan_datasd.csv',
        'council_districts': 'https://seshat.datasd.org/sde/council_districts_datasd.csv',
        'police_neighborhoods': 'https://seshat.datasd.org/pd/pd_neighborhoods_datasd.csv',
        'zoning': 'https://seshat.datasd.org/sde/zoning_datasd.csv',
    }
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.permits_data = None
        self.neighborhoods_data = None
        self.zoning_data = None
        self.pdf_content = None
        self.use_local = self._check_local_data()
        
    def _check_local_data(self) -> bool:
        """Check if local data directory exists and has files"""
        if not self.data_dir.exists():
            return False
        
        # Check if we have any CSV files locally
        csv_files = list(self.data_dir.rglob("*.csv"))
        return len(csv_files) > 0
    
    def load_all_data(self):
        """Load all available data sources"""
        mode = "local files" if self.use_local else "remote URLs"
        print(f"Loading San Diego data from {mode}...")
        
        # Load CSV data
        self.load_permits()
        self.load_neighborhoods()
        self.load_zoning()
        
        # Load PDF if it exists (local only)
        self.load_pdf_documents()
        
        print("✅ All data loaded successfully!")
        return self
    
    def _load_csv(self, local_path: Path, url_key: str, description: str) -> Optional[pd.DataFrame]:
        """
        Load CSV from local file if available, otherwise from URL
        
        Args:
            local_path: Path to local CSV file
            url_key: Key in DATA_URLS dict
            description: Description for logging
        
        Returns:
            DataFrame or None if loading fails
        """
        try:
            if self.use_local and local_path.exists():
                print(f"Loading {description} from local file: {local_path}")
                df = pd.read_csv(local_path, low_memory=False)
                print(f"  ✓ Loaded {len(df)} rows")
                return df
            elif url_key in self.DATA_URLS:
                print(f"Downloading {description} from URL...")
                df = pd.read_csv(self.DATA_URLS[url_key], low_memory=False)
                print(f"  ✓ Downloaded {len(df)} rows")
                return df
            else:
                print(f"  ⚠️  No source available for {description}")
                return None
        except Exception as e:
            print(f"  ✗ Error loading {description}: {e}")
            return None
    
    def load_permits(self):
        """Load development permit data"""
        permits_dir = self.data_dir / "permits"
        data = {}
        
        # Load active permits - try multiple locations
        active_paths = [
            self.data_dir / "permits_set2_active_datasd.csv",  # Root level (actual location)
            permits_dir / "active_approvals.csv",
            permits_dir / "permits_set2_active_datasd.csv"
        ]
        
        df = None
        for path in active_paths:
            if path.exists():
                df = self._load_csv(path, 'permits_active', 'active permits')
                break
        
        if df is None and 'permits_active' in self.DATA_URLS:
            df = self._load_csv(Path("nonexistent"), 'permits_active', 'active permits')
        
        if df is not None:
            data['active'] = df
        
        # Load closed permits
        closed_paths = [
            self.data_dir / "permits_set2_closed_datasd.csv",  # Root level (actual location)
            permits_dir / "closed_approvals.csv",
            permits_dir / "permits_set2_closed_datasd.csv"
        ]
        
        df = None
        for path in closed_paths:
            if path.exists():
                df = self._load_csv(path, 'permits_closed', 'closed permits')
                break
        
        if df is None and 'permits_closed' in self.DATA_URLS:
            df = self._load_csv(Path("nonexistent"), 'permits_closed', 'closed permits')
        
        if df is not None:
            data['closed'] = df
        
        # Load permit tags
        tags_paths = [
            self.data_dir / "permits_project_tags_datasd.csv",  # Root level (actual location)
            permits_dir / "permit_tags.csv",
            permits_dir / "permits_project_tags_datasd.csv"
        ]
        
        for path in tags_paths:
            if path.exists():
                try:
                    print(f"Loading permit tags from {path}...")
                    data['tags'] = pd.read_csv(path, low_memory=False)
                    print(f"  ✓ Loaded {len(data['tags'])} permit tags")
                    break
                except Exception as e:
                    print(f"  ✗ Error loading permit tags: {e}")
        
        self.permits_data = data
        return data
    
    def load_neighborhoods(self):
        """Load neighborhood and community data"""
        neighborhoods_dir = self.data_dir / "neighborhoods"
        data = {}
        
        # Load community planning districts
        # Try multiple possible locations and names
        cpd_paths = [
            self.data_dir / "cmty_plan_datasd.csv",  # Root level (actual location)
            neighborhoods_dir / "community_planning_districts.csv",
            neighborhoods_dir / "cmty_plan_datasd.csv"
        ]
        
        df = None
        for path in cpd_paths:
            if path.exists():
                df = self._load_csv(path, 'communities', 'community planning districts')
                break
        
        if df is None and 'communities' in self.DATA_URLS:
            # Try URL as fallback
            df = self._load_csv(Path("nonexistent"), 'communities', 'community planning districts')
        
        if df is not None:
            data['communities'] = df
        
        # Load council districts
        council_paths = [
            self.data_dir / "council_districts_datasd.csv",  # Root level (actual location)
            neighborhoods_dir / "council_districts.csv",
            neighborhoods_dir / "council_districts_datasd.csv"
        ]
        
        df = None
        for path in council_paths:
            if path.exists():
                df = self._load_csv(path, 'council_districts', 'council districts')
                break
        
        if df is None and 'council_districts' in self.DATA_URLS:
            df = self._load_csv(Path("nonexistent"), 'council_districts', 'council districts')
        
        if df is not None:
            data['council_districts'] = df
        
        # Load police neighborhoods
        police_paths = [
            self.data_dir / "pd_neighborhoods_datasd.csv",  # Root level (actual location)
            neighborhoods_dir / "police_neighborhoods.csv",
            neighborhoods_dir / "pd_neighborhoods_datasd.csv"
        ]
        
        df = None
        for path in police_paths:
            if path.exists():
                df = self._load_csv(path, 'police_neighborhoods', 'police neighborhoods')
                break
        
        if df is None and 'police_neighborhoods' in self.DATA_URLS:
            df = self._load_csv(Path("nonexistent"), 'police_neighborhoods', 'police neighborhoods')
        
        if df is not None:
            data['police_neighborhoods'] = df
        
        self.neighborhoods_data = data
        return data
    
    def load_zoning(self):
        """Load zoning data"""
        zoning_dir = self.data_dir / "zoning"
        data = {}
        
        # Load zoning designations - try multiple locations
        zoning_paths = [
            self.data_dir / "zoning_datasd.csv",  # Root level (actual location)
            zoning_dir / "zoning_designations.csv",
            zoning_dir / "zoning_datasd.csv"
        ]
        
        df = None
        for path in zoning_paths:
            if path.exists():
                df = self._load_csv(path, 'zoning', 'zoning designations')
                break
        
        if df is None and 'zoning' in self.DATA_URLS:
            df = self._load_csv(Path("nonexistent"), 'zoning', 'zoning designations')
        
        if df is not None:
            data['designations'] = df
        
        self.zoning_data = data
        return data
    
    def load_pdf_documents(self):
        """Load PDF municipal documents (local only)"""
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
        # Try different possible column names
        name_columns = ['cpname', 'name', 'community', 'CPNAME', 'NAME']
        name_column = None
        
        for col in name_columns:
            if col in communities.columns:
                name_column = col
                break
        
        if not name_column:
            return None
        
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
            name_columns = ['cpname', 'name', 'community', 'CPNAME', 'NAME']
            name_col = None
            for col in name_columns:
                if col in communities.columns:
                    name_col = col
                    break
            
            if name_col:
                community_list = communities[name_col].tolist()
                context_parts.append(f"San Diego has {len(community_list)} community planning districts:\n")
                context_parts.append(", ".join(str(c) for c in community_list[:50]))  # First 50
        
        return "\n".join(context_parts)
    
    def get_data_summary(self) -> Dict:
        """Get a summary of all loaded data"""
        summary = {
            'permits': {},
            'neighborhoods': {},
            'zoning': {},
            'documents': {},
            'data_source': 'local files' if self.use_local else 'remote URLs'
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