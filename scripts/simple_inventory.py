#!/usr/bin/env python3
"""
simple_inventory.py - Simplified data source inventory management

Manages a streamlined inventory with these fields:
- Source ID: Unique identifier (e.g., ESTAT_001)
- Topic: Subject area (e.g., Transport, Economics, Environment)
- Source Name: Name of the data source
- URL: Web address or access method
- Date Accessed: When data was last accessed (YYYY-MM-DD)
- Data Years: Time period covered (e.g., 2005-2023)
- Geographic Scope: Geographic coverage (e.g., EU, BE, NL)
- File Location: Path to local file(s)
- Data Format: File format (CSV, TSV, Excel, JSON, etc.)
- Key Variables: Main variables/columns in the dataset
- Data Quality: Quality rating (1-5 stars) and notes
- Limitations: Known limitations or issues
- Update Frequency: How often source is updated
- Contact Info: Contact person or organization
- Notes: Additional information
"""

import argparse
import sys
from pathlib import Path
from datetime import date
from typing import Optional, List, Dict
import pandas as pd


class SimpleInventory:
    """Manage simplified data source inventory"""

    FIELDS = [
        'Source ID',
        'Topic',
        'Source Name',
        'URL',
        'Date Accessed',
        'Data Years',
        'Geographic Scope',
        'File Location',
        'Data Format',
        'Key Variables',
        'Data Quality',
        'Limitations',
        'Update Frequency',
        'Contact Info',
        'Notes'
    ]

    TOPICS = [
        'Transport',
        'Economics',
        'Environment',
        'Fleet Management',
        'Operations',
        'Labor Market',
        'Infrastructure',
        'Safety',
        'Digitalization',
        'Other'
    ]

    DATA_FORMATS = [
        'CSV',
        'TSV',
        'Excel',
        'JSON',
        'XML',
        'Database',
        'API',
        'PDF',
        'Other'
    ]

    UPDATE_FREQUENCIES = [
        'Real-time',
        'Daily',
        'Weekly',
        'Monthly',
        'Quarterly',
        'Annual',
        'Ad-hoc',
        'Static'
    ]

    def __init__(self, inventory_path: Path):
        """Initialize inventory manager"""
        self.inventory_path = inventory_path
        self.df = None

    def load(self):
        """Load existing inventory or create new one"""
        if self.inventory_path.exists():
            print(f"Loading inventory from: {self.inventory_path}")
            if self.inventory_path.suffix == '.xlsx':
                self.df = pd.read_excel(self.inventory_path)
            else:
                self.df = pd.read_csv(self.inventory_path)
            print(f"  Loaded {len(self.df)} entries")
        else:
            print("Creating new inventory...")
            self.df = pd.DataFrame(columns=self.FIELDS)

    def save(self):
        """Save inventory"""
        print(f"Saving inventory to: {self.inventory_path}")

        if self.inventory_path.suffix == '.xlsx':
            self.df.to_excel(self.inventory_path, index=False)
        else:
            self.df.to_csv(self.inventory_path, index=False)

        print(f"  ✓ Saved {len(self.df)} entries")

    def add_entry(self, entry: Dict[str, str], interactive: bool = False):
        """Add a new entry to inventory"""

        if interactive:
            entry = self._interactive_entry(entry)

        # Validate source ID is unique
        if 'Source ID' in entry and not pd.isna(entry['Source ID']):
            if entry['Source ID'] in self.df['Source ID'].values:
                print(f"Warning: Source ID '{entry['Source ID']}' already exists!")
                overwrite = input("Overwrite existing entry? (y/n): ").strip().lower()
                if overwrite == 'y':
                    self.df = self.df[self.df['Source ID'] != entry['Source ID']]
                else:
                    print("Cancelled.")
                    return False

        # Add entry
        new_row = pd.DataFrame([entry])
        self.df = pd.concat([self.df, new_row], ignore_index=True)

        print(f"✓ Added: {entry.get('Source ID', 'NEW')} - {entry.get('Source Name', 'Unnamed')}")
        return True

    def _interactive_entry(self, initial_data: Dict = None) -> Dict[str, str]:
        """Interactively collect entry data"""
        if initial_data is None:
            initial_data = {}

        entry = {}

        print("\n" + "="*80)
        print("ADD NEW DATA SOURCE")
        print("="*80)
        print("(Press Enter to skip optional fields)\n")

        # Source ID (required)
        while True:
            default = initial_data.get('Source ID', '')
            source_id = input(f"Source ID [required] [{default}]: ").strip() or default
            if source_id:
                entry['Source ID'] = source_id
                break
            print("  Source ID is required!")

        # Topic (with suggestions)
        print(f"\nSuggested topics: {', '.join(self.TOPICS)}")
        default = initial_data.get('Topic', '')
        entry['Topic'] = input(f"Topic [{default}]: ").strip() or default

        # Source Name (required)
        while True:
            default = initial_data.get('Source Name', '')
            source_name = input(f"Source Name [required] [{default}]: ").strip() or default
            if source_name:
                entry['Source Name'] = source_name
                break
            print("  Source Name is required!")

        # URL
        default = initial_data.get('URL', '')
        entry['URL'] = input(f"URL [{default}]: ").strip() or default

        # Date Accessed (default to today)
        default = initial_data.get('Date Accessed', str(date.today()))
        entry['Date Accessed'] = input(f"Date Accessed (YYYY-MM-DD) [{default}]: ").strip() or default

        # Data Years
        default = initial_data.get('Data Years', '')
        entry['Data Years'] = input(f"Data Years (e.g., 2005-2023) [{default}]: ").strip() or default

        # Geographic Scope
        default = initial_data.get('Geographic Scope', '')
        entry['Geographic Scope'] = input(f"Geographic Scope (e.g., BE, EU) [{default}]: ").strip() or default

        # File Location
        default = initial_data.get('File Location', '')
        entry['File Location'] = input(f"File Location (path to file) [{default}]: ").strip() or default

        # Data Format
        print(f"\nCommon formats: {', '.join(self.DATA_FORMATS)}")
        default = initial_data.get('Data Format', '')
        entry['Data Format'] = input(f"Data Format [{default}]: ").strip() or default

        # Key Variables
        default = initial_data.get('Key Variables', '')
        entry['Key Variables'] = input(f"Key Variables (comma-separated) [{default}]: ").strip() or default

        # Data Quality (1-5 stars)
        while True:
            default = initial_data.get('Data Quality', '')
            quality = input(f"Data Quality (1-5 stars or description) [{default}]: ").strip() or default
            if quality:
                entry['Data Quality'] = quality
                break
            else:
                break

        # Limitations
        default = initial_data.get('Limitations', '')
        entry['Limitations'] = input(f"Limitations [{default}]: ").strip() or default

        # Update Frequency
        print(f"\nFrequencies: {', '.join(self.UPDATE_FREQUENCIES)}")
        default = initial_data.get('Update Frequency', '')
        entry['Update Frequency'] = input(f"Update Frequency [{default}]: ").strip() or default

        # Contact Info
        default = initial_data.get('Contact Info', '')
        entry['Contact Info'] = input(f"Contact Info [{default}]: ").strip() or default

        # Notes
        default = initial_data.get('Notes', '')
        entry['Notes'] = input(f"Notes [{default}]: ").strip() or default

        return entry

    def list_entries(self, topic: Optional[str] = None):
        """List all entries, optionally filtered by topic"""
        print("\n" + "="*80)
        print("DATA SOURCE INVENTORY")
        print("="*80)

        df = self.df
        if topic:
            df = df[df['Topic'].str.contains(topic, case=False, na=False)]
            print(f"Filtered by topic: {topic}")

        if len(df) == 0:
            print("No entries found.")
            return

        print(f"\nTotal entries: {len(df)}\n")

        # Display compact view
        for idx, row in df.iterrows():
            print(f"[{row['Source ID']}] {row['Source Name']}")
            print(f"  Topic: {row['Topic']} | Format: {row['Data Format']} | Years: {row['Data Years']}")
            print(f"  Location: {row['File Location']}")
            print()

    def show_entry(self, source_id: str):
        """Show detailed view of a single entry"""
        entry = self.df[self.df['Source ID'] == source_id]

        if len(entry) == 0:
            print(f"Entry not found: {source_id}")
            return

        print("\n" + "="*80)
        print(f"DATA SOURCE: {source_id}")
        print("="*80 + "\n")

        entry = entry.iloc[0]
        for field in self.FIELDS:
            value = entry.get(field, '')
            if pd.notna(value) and value != '':
                print(f"{field:20s}: {value}")

    def delete_entry(self, source_id: str):
        """Delete an entry"""
        if source_id not in self.df['Source ID'].values:
            print(f"Entry not found: {source_id}")
            return False

        self.df = self.df[self.df['Source ID'] != source_id]
        print(f"✓ Deleted: {source_id}")
        return True

    def search(self, keyword: str):
        """Search inventory by keyword"""
        print(f"\nSearching for: '{keyword}'")

        # Search across all text fields
        mask = self.df.astype(str).apply(
            lambda row: row.str.contains(keyword, case=False, na=False).any(),
            axis=1
        )

        results = self.df[mask]

        if len(results) == 0:
            print("No matches found.")
            return

        print(f"Found {len(results)} matches:\n")

        for idx, row in results.iterrows():
            print(f"[{row['Source ID']}] {row['Source Name']}")
            print(f"  Topic: {row['Topic']}")
            print()

    def export_template(self, output_path: Path):
        """Export an empty template"""
        template = pd.DataFrame(columns=self.FIELDS)

        # Add example row
        example = {
            'Source ID': 'EXAMPLE_001',
            'Topic': 'Transport',
            'Source Name': 'Example Data Source',
            'URL': 'https://example.com/data',
            'Date Accessed': str(date.today()),
            'Data Years': '2020-2023',
            'Geographic Scope': 'BE',
            'File Location': 'data/example.csv',
            'Data Format': 'CSV',
            'Key Variables': 'variable1, variable2, variable3',
            'Data Quality': '4 stars - Reliable with minor gaps',
            'Limitations': 'Annual data only, no sub-regional breakdown',
            'Update Frequency': 'Annual',
            'Contact Info': 'data@example.org',
            'Notes': 'This is an example entry. Delete this row.'
        }

        template = pd.DataFrame([example])

        if output_path.suffix == '.xlsx':
            template.to_excel(output_path, index=False)
        else:
            template.to_csv(output_path, index=False)

        print(f"✓ Template exported to: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description='Simple data source inventory management',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        '--inventory',
        type=Path,
        default=Path('data_inventory.csv'),
        help='Path to inventory file (default: data_inventory.csv)'
    )

    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # Add command
    add_parser = subparsers.add_parser('add', help='Add new data source')
    add_parser.add_argument('--interactive', '-i', action='store_true', help='Interactive mode')
    add_parser.add_argument('--source-id', help='Source ID')
    add_parser.add_argument('--topic', help='Topic')
    add_parser.add_argument('--name', help='Source name')
    add_parser.add_argument('--url', help='URL')
    add_parser.add_argument('--file', help='File location')
    add_parser.add_argument('--format', help='Data format')
    add_parser.add_argument('--years', help='Data years')
    add_parser.add_argument('--geo', help='Geographic scope')

    # List command
    list_parser = subparsers.add_parser('list', help='List all entries')
    list_parser.add_argument('--topic', help='Filter by topic')

    # Show command
    show_parser = subparsers.add_parser('show', help='Show entry details')
    show_parser.add_argument('source_id', help='Source ID to show')

    # Delete command
    delete_parser = subparsers.add_parser('delete', help='Delete entry')
    delete_parser.add_argument('source_id', help='Source ID to delete')

    # Search command
    search_parser = subparsers.add_parser('search', help='Search inventory')
    search_parser.add_argument('keyword', help='Search keyword')

    # Template command
    template_parser = subparsers.add_parser('template', help='Export empty template')
    template_parser.add_argument('output', type=Path, help='Output file path')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    # Handle template command (doesn't need to load inventory)
    if args.command == 'template':
        inventory = SimpleInventory(args.inventory)
        inventory.export_template(args.output)
        return 0

    # Load inventory
    inventory = SimpleInventory(args.inventory)
    inventory.load()

    # Execute command
    if args.command == 'add':
        initial_data = {
            'Source ID': args.source_id,
            'Topic': args.topic,
            'Source Name': args.name,
            'URL': args.url,
            'File Location': args.file,
            'Data Format': args.format,
            'Data Years': args.years,
            'Geographic Scope': args.geo,
        }
        # Remove None values
        initial_data = {k: v for k, v in initial_data.items() if v is not None}

        if inventory.add_entry(initial_data, interactive=args.interactive or len(initial_data) == 0):
            inventory.save()

    elif args.command == 'list':
        inventory.list_entries(args.topic)

    elif args.command == 'show':
        inventory.show_entry(args.source_id)

    elif args.command == 'delete':
        if inventory.delete_entry(args.source_id):
            inventory.save()

    elif args.command == 'search':
        inventory.search(args.keyword)

    return 0


if __name__ == '__main__':
    exit(main())
