import urllib.request
import json

print("=== VERIFYING SERVICES ===")

# 1. Test frontend
try:
    with urllib.request.urlopen('http://127.0.0.1:5173/') as r:
        html = r.read().decode('utf-8')
        print(f"[SUCCESS] Frontend online at http://127.0.0.1:5173 (Status: {r.status})")
        print(f"          Title verified: {'OmniHealth' in html}")
except Exception as e:
    print(f"[ERROR] Frontend check failed: {e}")

# 2. Test backend
try:
    with urllib.request.urlopen('http://127.0.0.1:5000/api/status') as r:
        status_data = json.loads(r.read())
        print(f"[SUCCESS] Backend API online at http://127.0.0.1:5000/api/status (Status: {r.status})")
        print(f"          Loaded models: {status_data.get('models_loaded')}")

    with urllib.request.urlopen('http://127.0.0.1:5000/api/models-info') as r:
        models_data = json.loads(r.read())
        print("[SUCCESS] Models Performance Telemetry:")
        for disease, m in models_data['metrics'].items():
            print(f"          • {m['name']}: Accuracy = {m['accuracy']*100:.2f}%, F1 = {m['f1_score']:.4f}, Recall = {m['recall']*100:.2f}%")
except Exception as e:
    print(f"[ERROR] Backend check failed: {e}")

print("=== VERIFICATION COMPLETE ===")
