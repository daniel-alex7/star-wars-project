import requests
import time
from flask import jsonify

def swapi_proxy(request):
    start_time = time.time()
    base_url = f"https://{request.host}/consultar"
    api_key = request.args.get('key', '')
    
    categoria = request.args.get('categoria', 'people')
    item_id = request.args.get('id', '')
    
    
    swapi_url = f"https://swapi.dev/api/{categoria}/{item_id}"
    
    try:
        response = requests.get(swapi_url, timeout=10)
        data = response.json()

        
        actions = []
        if not item_id:  # Se for uma lista
            actions.append({"rel": "self", "method": "GET", "href": f"{base_url}?key={api_key}&categoria={categoria}"})
            actions.append({"rel": "filter_by_id", "description": "Adicione '&id=1' para ver detalhes"})
        else: 
            actions.append({"rel": "list_all", "method": "GET", "href": f"{base_url}?key={api_key}&categoria={categoria}"})
            
        
        suggestions = {
            "people": ["planets", "starships"],
            "films": ["characters", "planets"],
            "planets": ["residents"]
        }

        duration = time.time() - start_time
        
       
        output = {
            "api_version": "v9.0-advanced",
            "metadata": {
                "execution_time": f"{duration:.3f}s",
                "total_results": data.get('count') if 'count' in data else 1
            },
            "ui_navigation": {  # <--- Aqui está a sua "Interface"
                "current_category": categoria,
                "available_actions": actions,
                "quick_explore": [f"{base_url}?key={api_key}&categoria={s}" for s in suggestions.get(categoria, [])]
            },
            "payload": data
        }
        
        return jsonify(output), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500