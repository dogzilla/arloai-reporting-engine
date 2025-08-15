"""
Data processors for handling various input formats.
"""

from typing import Dict, List, Union, Any
from pathlib import Path
import logging
import pandas as pd

logger = logging.getLogger(__name__)


class DataProcessor:
    """
    Main data processor that handles various input formats and
    normalizes them into a standard format for widgets.
    """
    
    def __init__(self):
        """Initialize the data processor."""
        self.processors = {
            '.xlsx': self._process_excel,
            '.xls': self._process_excel,
            '.csv': self._process_csv,
            '.pdf': self._process_pdf,
            '.json': self._process_json
        }
    
    def process_sources(self, sources: List[Union[str, Path]]) -> Dict[str, Any]:
        """
        Process multiple data sources and combine into normalized format.
        
        Args:
            sources: List of file paths to process
            
        Returns:
            Dictionary with normalized data
        """
        logger.info(f"Processing {len(sources)} data sources")
        
        combined_data = {
            'metrics': {},
            'time_series': {},
            'dimensions': {},
            'metadata': {}
        }
        
        for source in sources:
            source_path = Path(source)
            if not source_path.exists():
                logger.warning(f"Source file not found: {source}")
                continue
            
            try:
                source_data = self._process_single_source(source_path)
                combined_data = self._merge_data(combined_data, source_data)
                logger.debug(f"Processed source: {source}")
            except Exception as e:
                logger.error(f"Error processing {source}: {e}")
        
        return combined_data
    
    def _process_single_source(self, source_path: Path) -> Dict[str, Any]:
        """
        Process a single data source file.
        
        Args:
            source_path: Path to the source file
            
        Returns:
            Dictionary with processed data
        """
        suffix = source_path.suffix.lower()
        processor = self.processors.get(suffix)
        
        if not processor:
            raise ValueError(f"Unsupported file format: {suffix}")
        
        return processor(source_path)
    
    def _process_excel(self, file_path: Path) -> Dict[str, Any]:
        """Process Excel files (.xlsx, .xls)."""
        logger.debug(f"Processing Excel file: {file_path}")
        
        try:
            # Read all sheets
            excel_data = pd.read_excel(file_path, sheet_name=None)
            
            processed_data = {
                'metrics': {},
                'time_series': {},
                'dimensions': {},
                'metadata': {
                    'source_file': str(file_path),
                    'source_type': 'excel',
                    'sheets': list(excel_data.keys())
                }
            }
            
            # Process each sheet
            for sheet_name, df in excel_data.items():
                sheet_data = self._process_dataframe(df, sheet_name)
                processed_data = self._merge_data(processed_data, sheet_data)
            
            return processed_data
            
        except Exception as e:
            logger.error(f"Error processing Excel file {file_path}: {e}")
            return self._empty_data_structure()
    
    def _process_csv(self, file_path: Path) -> Dict[str, Any]:
        """Process CSV files."""
        logger.debug(f"Processing CSV file: {file_path}")
        
        try:
            df = pd.read_csv(file_path)
            return self._process_dataframe(df, file_path.stem)
        except Exception as e:
            logger.error(f"Error processing CSV file {file_path}: {e}")
            return self._empty_data_structure()
    
    def _process_pdf(self, file_path: Path) -> Dict[str, Any]:
        """Process PDF files (placeholder implementation)."""
        logger.debug(f"Processing PDF file: {file_path}")
        
        # Placeholder - in practice, this would extract data from PDF
        return {
            'metrics': {},
            'time_series': {},
            'dimensions': {},
            'metadata': {
                'source_file': str(file_path),
                'source_type': 'pdf',
                'note': 'PDF processing not yet implemented'
            }
        }
    
    def _process_json(self, file_path: Path) -> Dict[str, Any]:
        """Process JSON files."""
        logger.debug(f"Processing JSON file: {file_path}")
        
        try:
            import json
            with open(file_path, 'r') as f:
                json_data = json.load(f)
            
            return {
                'metrics': json_data.get('metrics', {}),
                'time_series': json_data.get('time_series', {}),
                'dimensions': json_data.get('dimensions', {}),
                'metadata': {
                    'source_file': str(file_path),
                    'source_type': 'json',
                    **json_data.get('metadata', {})
                }
            }
        except Exception as e:
            logger.error(f"Error processing JSON file {file_path}: {e}")
            return self._empty_data_structure()
    
    def _process_dataframe(self, df: pd.DataFrame, source_name: str) -> Dict[str, Any]:
        """
        Process a pandas DataFrame into normalized format.
        
        Args:
            df: DataFrame to process
            source_name: Name/identifier for the data source
            
        Returns:
            Dictionary with normalized data
        """
        processed_data = {
            'metrics': {},
            'time_series': {},
            'dimensions': {},
            'metadata': {
                'source_name': source_name,
                'rows': len(df),
                'columns': list(df.columns)
            }
        }
        
        # Detect time series data (columns with date-like names or datetime types)
        date_columns = []
        for col in df.columns:
            if df[col].dtype == 'datetime64[ns]' or 'date' in col.lower():
                date_columns.append(col)
        
        if date_columns:
            # Process as time series data
            for date_col in date_columns:
                processed_data['time_series'][f'{source_name}_{date_col}'] = {
                    'dates': df[date_col].tolist(),
                    'data': df.drop(columns=date_columns).to_dict('records')
                }
        
        # Extract numeric metrics
        numeric_columns = df.select_dtypes(include=['number']).columns
        if len(numeric_columns) > 0:
            processed_data['metrics'][source_name] = df[numeric_columns].describe().to_dict()
        
        # Extract categorical dimensions
        categorical_columns = df.select_dtypes(include=['object', 'category']).columns
        if len(categorical_columns) > 0:
            for col in categorical_columns:
                if col not in date_columns:
                    processed_data['dimensions'][f'{source_name}_{col}'] = df[col].value_counts().to_dict()
        
        return processed_data
    
    def _merge_data(self, target: Dict[str, Any], source: Dict[str, Any]) -> Dict[str, Any]:
        """
        Merge source data into target data structure.
        
        Args:
            target: Target data dictionary
            source: Source data dictionary to merge
            
        Returns:
            Merged data dictionary
        """
        for key in ['metrics', 'time_series', 'dimensions', 'metadata']:
            if key in source:
                target[key].update(source[key])
        
        return target
    
    def _empty_data_structure(self) -> Dict[str, Any]:
        """Return empty data structure."""
        return {
            'metrics': {},
            'time_series': {},
            'dimensions': {},
            'metadata': {}
        }