import os
import sys
ROOT = os.path.abspath(os.path.dirname(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from app import create_app

app = create_app()

for rule in sorted(app.url_map.iter_rules(), key=lambda r: r.rule):
    methods = ",".join(sorted(rule.methods - {"HEAD", "OPTIONS"}))
    print(f"{rule.rule} -> methods: [{methods}] -> endpoint: {rule.endpoint}")
