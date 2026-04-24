import json

# Define the diagram for KCl (Ionic Bond)
kcl_diag = """
<div style="background: #f8f9fa; padding: 20px; border-radius: 12px; border: 1px solid #e9ecef; margin-bottom: 15px;">
  <div style="font-weight: bold; color: #2c3e50; margin-bottom: 10px;">Sơ đồ hình thành liên kết KCl (Ion):</div>
  <svg viewBox="0 0 400 150" xmlns="http://www.w3.org/2000/svg">
    <!-- K atom -->
    <circle cx="80" cy="75" r="40" fill="#FFEAA7" stroke="#F1C40F" stroke-width="2" />
    <text x="80" y="80" font-family="Arial" font-size="20" text-anchor="middle" font-weight="bold">K</text>
    <text x="80" y="130" font-family="Arial" font-size="12" text-anchor="middle">Nguyên tử K</text>
    
    <!-- Electron being transferred -->
    <circle cx="130" cy="75" r="5" fill="#FF7675" />
    <path d="M 140 75 L 240 75" stroke="#FF7675" stroke-width="2" marker-end="url(#arrowhead)" fill="none" />
    <defs>
      <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="0" refY="3.5" orient="auto">
        <polygon points="0 0, 10 3.5, 0 7" fill="#FF7675" />
      </marker>
    </defs>
    
    <!-- Cl atom -->
    <circle cx="320" cy="75" r="40" fill="#81ECEC" stroke="#00CEC9" stroke-width="2" />
    <text x="320" y="80" font-family="Arial" font-size="20" text-anchor="middle" font-weight="bold">Cl</text>
    <text x="320" y="130" font-family="Arial" font-size="12" text-anchor="middle">Nguyên tử Cl</text>
  </svg>
  
  <div style="display: flex; justify-content: space-between; margin-top: 10px; font-size: 0.9rem; color: #636e72;">
    <span>K nhường 1 electron</span>
    <span>Cl nhận 1 electron</span>
  </div>
  
  <div style="text-align: center; font-weight: bold; margin-top: 15px; color: #d63031;">
    K⁺ + Cl⁻ → KCl
  </div>
</div>
"""

# Update the problem in problems.js
file_path = r"d:\toanvui-main\toanvui-main\src\data\problems.js"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# I need to find the "g7-khtn-c1-e1" block and insert solutionIllustration
import re
pattern = r'("g7-khtn-c1-e1":\s*\{[^}]*?)(\s*"type": "essay")'
replacement = r'\1\n    "solutionIllustration": ' + json.dumps(kcl_diag, ensure_ascii=False) + r',\2'

updated_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(updated_content)

print("Successfully added diagram to g7-khtn-c1-e1.")
