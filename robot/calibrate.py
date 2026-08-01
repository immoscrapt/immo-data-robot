import json
import pyautogui

print("=" * 50)
print("CALIBRATION DU ROBOT")
print("=" * 50)

positions = {}

elements = [
    "DPE",
    "Recherche",
    "Champ commune",
    "Premier résultat"
]

for element in elements:
    input(f"\nPlace la souris sur [{element}] puis appuie sur Entrée...")
    x, y = pyautogui.position()
    positions[element] = {"x": x, "y": y}
    print(f"✅ {element} = ({x}, {y})")

with open("robot/calibration.json", "w") as f:
    json.dump(positions, f, indent=4)

print("\n🎉 Calibration terminée !")
print("Le fichier robot/calibration.json a été créé.")