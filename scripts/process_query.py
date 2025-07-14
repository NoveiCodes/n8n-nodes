#!/usr/bin/env python3
import json
import argparse
import requests
import sys
from typing import Dict, List, Any

def load_database():
    """Load the database from db.json"""
    try:
        with open('nodes/db.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Error: db.json not found")
        sys.exit(1)
    except json.JSONDecodeError:
        print("Error: Invalid JSON in db.json")
        sys.exit(1)

def search_nodes(db: Dict, search_term: str, limit: int = 10) -> List[Dict]:
    """Search for nodes by name, display_name, description, or package_name"""
    results = []
    search_term = search_term.lower()
    
    for node_key, node_data in db.items():
        if isinstance(node_data, dict):
            match_type = None
            
            # Search in node key
            if search_term in node_key.lower():
                match_type = 'key'
            # Search in display_name
            elif 'display_name' in node_data and search_term in node_data['display_name'].lower():
                match_type = 'display_name'
            # Search in description
            elif 'description' in node_data and search_term in node_data['description'].lower():
                match_type = 'description'
            # Search in package_name
            elif 'package_name' in node_data and search_term in node_data['package_name'].lower():
                match_type = 'package_name'
            
            if match_type:
                results.append({
                    'key': node_key,
                    'data': node_data,
                    'match_type': match_type
                })
    
    return results[:limit]

def filter_nodes(db: Dict, filters: Dict) -> List[Dict]:
    """Filter nodes based on criteria"""
    results = []
    
    for node_key, node_data in db.items():
        if isinstance(node_data, dict):
            match = True
            
            for filter_key, filter_value in filters.items():
                if filter_key in node_data:
                    if isinstance(filter_value, list):
                        if node_data[filter_key] not in filter_value:
                            match = False
                            break
                    else:
                        if node_data[filter_key] != filter_value:
                            match = False
                            break
                else:
                    match = False
                    break
            
            if match:
                results.append({
                    'key': node_key,
                    'data': node_data
                })
    
    return results

def get_node_by_key(db: Dict, key: str) -> Dict:
    """Get a specific node by key"""
    if key in db:
        return {
            'key': key,
            'data': db[key],
            'found': True
        }
    else:
        return {
            'key': key,
            'found': False,
            'error': 'Node not found'
        }

def get_node_categories(db: Dict) -> List[str]:
    """Get all unique categories"""
    categories = set()
    for node_data in db.values():
        if isinstance(node_data, dict) and 'category' in node_data:
            categories.add(node_data['category'])
    return sorted(list(categories))

def get_statistics(db: Dict) -> Dict:
    """Get database statistics"""
    stats = {
        'total_nodes': len(db),
        'categories': {},
        'node_types': {},
        'ai_tools': 0,
        'triggers': 0,
        'webhooks': 0,
        'versioned': 0,
        'development_styles': {}
    }
    
    for node_data in db.values():
        if isinstance(node_data, dict):
            # Count categories
            if 'category' in node_data:
                category = node_data['category']
                stats['categories'][category] = stats['categories'].get(category, 0) + 1
            
            # Count node types
            if 'node_type' in node_data:
                node_type = node_data['node_type']
                stats['node_types'][node_type] = stats['node_types'].get(node_type, 0) + 1
            
            # Count development styles
            if 'development_style' in node_data:
                style = node_data['development_style']
                stats['development_styles'][style] = stats['development_styles'].get(style, 0) + 1
            
            # Count boolean flags
            if node_data.get('is_ai_tool', False):
                stats['ai_tools'] += 1
            if node_data.get('is_trigger', False):
                stats['triggers'] += 1
            if node_data.get('is_webhook', False):
                stats['webhooks'] += 1
            if node_data.get('is_versioned', False):
                stats['versioned'] += 1
    
    return stats

def get_ai_tools(db: Dict) -> List[Dict]:
    """Get all AI tools"""
    return filter_nodes(db, {'is_ai_tool': True})

def get_triggers(db: Dict) -> List[Dict]:
    """Get all trigger nodes"""
    return filter_nodes(db, {'is_trigger': True})

def get_webhooks(db: Dict) -> List[Dict]:
    """Get all webhook nodes"""
    return filter_nodes(db, {'is_webhook': True})

def get_by_category(db: Dict, category: str) -> List[Dict]:
    """Get nodes by category"""
    return filter_nodes(db, {'category': category})

def get_by_development_style(db: Dict, style: str) -> List[Dict]:
    """Get nodes by development style"""
    return filter_nodes(db, {'development_style': style})

def process_query(query_type: str, query_params: Dict) -> Dict:
    """Process the query and return results"""
    db = load_database()
    
    try:
        if query_type == 'search':
            search_term = query_params.get('term', '')
            limit = query_params.get('limit', 10)
            results = search_nodes(db, search_term, limit)
            return {
                'success': True,
                'query_type': query_type,
                'results': results,
                'count': len(results)
            }
        
        elif query_type == 'filter':
            filters = query_params.get('filters', {})
            results = filter_nodes(db, filters)
            return {
                'success': True,
                'query_type': query_type,
                'results': results,
                'count': len(results)
            }
        
        elif query_type == 'get_node':
            key = query_params.get('key', '')
            result = get_node_by_key(db, key)
            return {
                'success': True,
                'query_type': query_type,
                'result': result
            }
        
        elif query_type == 'categories':
            categories = get_node_categories(db)
            return {
                'success': True,
                'query_type': query_type,
                'categories': categories,
                'count': len(categories)
            }
        
        elif query_type == 'statistics':
            stats = get_statistics(db)
            return {
                'success': True,
                'query_type': query_type,
                'statistics': stats
            }
        
        elif query_type == 'ai_tools':
            results = get_ai_tools(db)
            return {
                'success': True,
                'query_type': query_type,
                'results': results,
                'count': len(results)
            }
        
        elif query_type == 'triggers':
            results = get_triggers(db)
            return {
                'success': True,
                'query_type': query_type,
                'results': results,
                'count': len(results)
            }
        
        elif query_type == 'webhooks':
            results = get_webhooks(db)
            return {
                'success': True,
                'query_type': query_type,
                'results': results,
                'count': len(results)
            }
        
        elif query_type == 'by_category':
            category = query_params.get('category', '')
            results = get_by_category(db, category)
            return {
                'success': True,
                'query_type': query_type,
                'category': category,
                'results': results,
                'count': len(results)
            }
        
        elif query_type == 'by_development_style':
            style = query_params.get('style', '')
            results = get_by_development_style(db, style)
            return {
                'success': True,
                'query_type': query_type,
                'development_style': style,
                'results': results,
                'count': len(results)
            }
        
        else:
            return {
                'success': False,
                'error': f'Unknown query type: {query_type}'
            }
    
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def send_callback(callback_url: str, results: Dict):
    """Send results back to n8n via webhook"""
    if callback_url:
        try:
            response = requests.post(callback_url, json=results, timeout=30)
            response.raise_for_status()
            print(f"Successfully sent results to callback URL: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error sending callback: {e}")

def main():
    parser = argparse.ArgumentParser(description='Process database queries')
    parser.add_argument('--query-type', required=True, help='Type of query')
    parser.add_argument('--query-params', required=True, help='Query parameters as JSON')
    parser.add_argument('--callback-url', help='Callback URL for results')
    
    args = parser.parse_args()
    
    try:
        query_params = json.loads(args.query_params)
    except json.JSONDecodeError:
        print("Error: Invalid JSON in query parameters")
        sys.exit(1)
    
    # Process the query
    results = process_query(args.query_type, query_params)
    
    # Output results (GitHub Actions will capture this)
    print(json.dumps(results, indent=2))
    
    # Send callback if URL provided
    if args.callback_url:
        send_callback(args.callback_url, results)

if __name__ == '__main__':
    main()