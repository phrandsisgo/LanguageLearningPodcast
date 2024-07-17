import os
import json
from datetime import datetime

def generate_filename(title):
    """Generiert einen Dateinamen basierend auf Titel, Datum und Uhrzeit."""
    now = datetime.now()
    date_time = now.strftime("%Y%m%d-%H%M%S")
    return f"{title}-{date_time}"

def ensure_output_directory():
    """Stellt sicher, dass der Ausgabeordner existiert."""
    if not os.path.exists('output'):
        os.makedirs('output')

def save_output(title, content, token_usage):
    """Speichert den Inhalt und Token-Nutzung in einer Datei im Ausgabeordner mit generiertem Dateinamen."""
    ensure_output_directory()
    filename = generate_filename(title)
    full_path = os.path.join('output', f"{filename}.json")
    
    output_data = {
        "content": content,
        "token_usage": token_usage
    }
    
    with open(full_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    return full_path

def load_output(filepath):
    """Lädt den Inhalt aus einer spezifischen Datei."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def edit_content(filepath):
    """Öffnet eine Datei zur Bearbeitung und speichert die Änderungen."""
    data = load_output(filepath)
    content = data['content']
    
    print("Aktueller Inhalt:")
    for key, value in content.items():
        print(f"{key}: {value}")
    
    for key in content.keys():
        edited = input(f"Bearbeiten Sie den Inhalt von '{key}' (leer lassen für keine Änderung):\n")
        if edited:
            content[key] = edited
    
    data['content'] = content
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def analyze_output(filepath):
    """Analysiert den Inhalt einer Ausgabedatei und gibt Statistiken zurück."""
    data = load_output(filepath)
    content = data['content']
    token_usage = data['token_usage']
    
    stats = {
        "token_usage": token_usage,
        "content_stats": {}
    }
    
    for key, value in content.items():
        stats["content_stats"][key] = {
            'chars': len(value)
        }
    
    return stats

#nun kann ich diese Funktionen noch im Hauptskript folgendermassen verwenden:
#has to translated to english but I'm too tired to do it now
"""

import os
import json
from datetime import datetime

def generate_filename(title):
    "Generiert einen Dateinamen basierend auf Titel, Datum und Uhrzeit."
    now = datetime.now()
    date_time = now.strftime("%Y%m%d-%H%M%S")
    return f"{title}-{date_time}"

def ensure_output_directory():
    "Stellt sicher, dass der Ausgabeordner existiert."
    if not os.path.exists('output'):
        os.makedirs('output')

def save_output(title, content, token_usage):
    "Speichert den Inhalt und Token-Nutzung in einer Datei im Ausgabeordner mit generiertem Dateinamen."
    ensure_output_directory()
    filename = generate_filename(title)
    full_path = os.path.join('output', f"{filename}.json")
    
    output_data = {
        "content": content,
        "token_usage": token_usage
    }
    
    with open(full_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    return full_path

def load_output(filepath):
    "Lädt den Inhalt aus einer spezifischen Datei."
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def edit_content(filepath):
    "Öffnet eine Datei zur Bearbeitung und speichert die Änderungen."
    data = load_output(filepath)
    content = data['content']
    
    print("Aktueller Inhalt:")
    for key, value in content.items():
        print(f"{key}: {value}")
    
    for key in content.keys():
        edited = input(f"Bearbeiten Sie den Inhalt von '{key}' (leer lassen für keine Änderung):\n")
        if edited:
            content[key] = edited
    
    data['content'] = content
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def analyze_output(filepath):
    "Analysiert den Inhalt einer Ausgabedatei und gibt Statistiken zurück."
    data = load_output(filepath)
    content = data['content']
    token_usage = data['token_usage']
    
    stats = {
        "token_usage": token_usage,
        "content_stats": {}
    }
    
    for key, value in content.items():
        stats["content_stats"][key] = {
            'chars': len(value)
        }
    
    return stats

"""