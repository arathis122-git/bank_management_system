import importlib, sys

try:
    importlib.import_module('bank_project.wsgi')
    print("✅ OK: bank_project.wsgi imported successfully")
except Exception as e:
    print("❌ IMPORT-ERROR:", type(e).__name__, e)
    sys.exit(1)
