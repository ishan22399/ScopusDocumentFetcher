from flask import Flask, render_template, request, jsonify
import requests
import re

app = Flask(__name__)

# Replace with your API Key from Elsevier Developer Portal
API_KEY = 'd053e3cc5a91b8e6e31fedf5c4a30b86'

def validate_api_key():
    """Check if the API key is valid by making a simple test request"""
    url = "https://api.elsevier.com/content/search/scopus"
    headers = {
        "X-ELS-APIKey": API_KEY,
        "Accept": "application/json"
    }
    params = {
        "query": "TITLE(test)",
        "count": 1
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        print(f"API Key validation - Status Code: {response.status_code}")
        if response.status_code != 200:
            print(f"API Key validation failed: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"API Key validation error: {str(e)}")
        return False

def search_author_by_name(first_name, last_name, api_key):
    """Search for author by name to get author ID"""
    url = "https://api.elsevier.com/content/search/author"
    headers = {
        "X-ELS-APIKey": api_key,
        "Accept": "application/json"
    }
    
    # Construct query based on available names
    if first_name and last_name:
        query = f'AUTHFIRST({first_name}) AND AUTHLASTNAME({last_name})'
    elif last_name:
        query = f'AUTHLASTNAME({last_name})'
    elif first_name:
        query = f'AUTHFIRST({first_name})'
    else:
        return {'success': False, 'error': 'Please provide at least first name or last name'}
    
    params = {
        "query": query,
        "count": 10
    }
    
    try:
        print(f"Author search URL: {url}")
        print(f"Author search query: {query}")
        response = requests.get(url, headers=headers, params=params)
        print(f"Author search - Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            entries = data.get('search-results', {}).get('entry', [])
            
            if entries:
                # Return the first matching author
                author = entries[0]
                author_id = author.get('dc:identifier', '').replace('AUTHOR_ID:', '')
                return {
                    'success': True,
                    'author_id': author_id,
                    'author_name': author.get('preferred-name', {}).get('given-name', '') + ' ' + 
                                 author.get('preferred-name', {}).get('surname', ''),
                    'affiliation': author.get('affiliation-current', {}).get('affiliation-name', 'N/A')
                }
            else:
                return {'success': False, 'error': 'No authors found with the given name'}
        elif response.status_code == 401:
            print(f"Author search 401 error: {response.text}")
            return {'success': False, 'error': 'API Key is invalid or expired for Author Search API. Please check your Elsevier API key permissions.'}
        elif response.status_code == 429:
            return {'success': False, 'error': 'API rate limit exceeded. Please try again later.'}
        else:
            print(f"Author search error - Status: {response.status_code}, Response: {response.text}")
            return {'success': False, 'error': f'Author search failed. Status Code: {response.status_code}. Response: {response.text}'}
    except Exception as e:
        print(f"Author search exception: {str(e)}")
        return {'success': False, 'error': f'Error searching author: {str(e)}'}

def search_by_orcid(orcid, api_key):
    """Search for author by ORCID ID"""
    url = "https://api.elsevier.com/content/search/author"
    headers = {
        "X-ELS-APIKey": api_key,
        "Accept": "application/json"
    }
    params = {
        "query": f"ORCID({orcid})",
        "count": 1
    }
    
    try:
        print(f"ORCID search URL: {url}")
        print(f"ORCID search query: ORCID({orcid})")
        response = requests.get(url, headers=headers, params=params)
        print(f"ORCID search - Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            entries = data.get('search-results', {}).get('entry', [])
            
            if entries:
                author = entries[0]
                author_id = author.get('dc:identifier', '').replace('AUTHOR_ID:', '')
                return {
                    'success': True,
                    'author_id': author_id,
                    'author_name': author.get('preferred-name', {}).get('given-name', '') + ' ' + 
                                 author.get('preferred-name', {}).get('surname', ''),
                    'orcid': orcid
                }
            else:
                return {'success': False, 'error': 'No author found with the given ORCID'}
        elif response.status_code == 401:
            print(f"ORCID search 401 error: {response.text}")
            return {'success': False, 'error': 'API Key is invalid or expired for Author Search API. Please check your Elsevier API key permissions.'}
        elif response.status_code == 429:
            return {'success': False, 'error': 'API rate limit exceeded. Please try again later.'}
        else:
            print(f"ORCID search error - Status: {response.status_code}, Response: {response.text}")
            return {'success': False, 'error': f'ORCID search failed. Status Code: {response.status_code}. Response: {response.text}'}
    except Exception as e:
        print(f"ORCID search exception: {str(e)}")
        return {'success': False, 'error': f'Error searching ORCID: {str(e)}'}

def get_scopus_documents(author_id, api_key):
    """Fetch Scopus documents for a given author ID"""
    url = f"https://api.elsevier.com/content/search/scopus"
    headers = {
        "X-ELS-APIKey": api_key,
        "Accept": "application/json"
    }
    params = {
        "query": f"AU-ID({author_id})",
        "count": 25  # Adjust number of results per request
    }

    try:
        print(f"Scopus search URL: {url}")
        print(f"Scopus search query: AU-ID({author_id})")
        response = requests.get(url, headers=headers, params=params)
        print(f"Scopus search - Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            entries = data.get('search-results', {}).get('entry', [])
            
            # Process and format the data
            documents = []
            for entry in entries:
                doc = {
                    'title': entry.get('dc:title', 'N/A'),
                    'doi': entry.get('prism:doi', 'N/A'),
                    'journal': entry.get('prism:publicationName', 'N/A'),
                    'year': entry.get('prism:coverDate', 'N/A')[:4] if entry.get('prism:coverDate') else 'N/A',
                    'citation_count': entry.get('citedby-count', '0'),
                    'authors': entry.get('dc:creator', 'N/A'),
                    'abstract': entry.get('dc:description', 'No abstract available')
                }
                documents.append(doc)
            
            return {
                'success': True,
                'documents': documents,
                'total_count': len(documents)
            }
        elif response.status_code == 401:
            print(f"Scopus search 401 error: {response.text}")
            return {
                'success': False,
                'error': "API Key is invalid or expired for Scopus Search API. Please check your Elsevier API key permissions."
            }
        elif response.status_code == 429:
            return {
                'success': False,
                'error': "API rate limit exceeded. Please try again later."
            }
        else:
            print(f"Scopus search error - Status: {response.status_code}, Response: {response.text}")
            return {
                'success': False,
                'error': f"Failed to fetch data. Status Code: {response.status_code}",
                'details': response.text
            }
    except Exception as e:
        print(f"Scopus search exception: {str(e)}")
        return {
            'success': False,
            'error': f"An error occurred: {str(e)}"
        }

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search_documents():
    """API endpoint to search for documents"""
    data = request.get_json()
    
    # Get search parameters
    search_type = data.get('search_type', 'author_id')
    author_id = data.get('author_id', '').strip()
    first_name = data.get('first_name', '').strip()
    last_name = data.get('last_name', '').strip()
    orcid = data.get('orcid', '').strip()
    
    # Determine search method based on provided data
    final_author_id = None
    author_info = {}
    
    if search_type == 'name' and (first_name or last_name):
        # Search by name first to get author ID
        name_result = search_author_by_name(first_name, last_name, API_KEY)
        if name_result['success']:
            final_author_id = name_result['author_id']
            author_info = {
                'name': name_result.get('author_name', ''),
                'affiliation': name_result.get('affiliation', 'N/A')
            }
        else:
            return jsonify(name_result)
            
    elif search_type == 'orcid' and orcid:
        # Search by ORCID to get author ID
        orcid_result = search_by_orcid(orcid, API_KEY)
        if orcid_result['success']:
            final_author_id = orcid_result['author_id']
            author_info = {
                'name': orcid_result.get('author_name', ''),
                'orcid': orcid_result.get('orcid', '')
            }
        else:
            return jsonify(orcid_result)
            
    elif search_type == 'author_id' and author_id:
        # Direct author ID search
        final_author_id = author_id
        
    else:
        return jsonify({
            'success': False,
            'error': 'Please provide either Author ID, ORCID, or at least first/last name'
        })
    
    # Now search for documents using the author ID
    if final_author_id:
        result = get_scopus_documents(final_author_id, API_KEY)
        if result['success']:
            result['author_info'] = author_info
        return jsonify(result)
    else:
        return jsonify({
            'success': False,
            'error': 'Could not determine author ID'
        })

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
