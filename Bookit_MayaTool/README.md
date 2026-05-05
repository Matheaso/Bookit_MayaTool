# Bookit Tool (Book placement)

Created by Maciej Sojka

## Links:
- [Linkedin](https://www.linkedin.com/in/maciej-sojka-3a929310a/)
- [Portfolio Reel](https://www.youtube.com/watch?v=L5NtHcKGt9g)

---

## Requirements
 - Maya 2027
 - PySide6


---

## How to use:
1. Copy the launcher code below
2. Paste it into Maya Script Editor (Python tab)
3. (Optional) Drag it to the shelf for quick access
4. Run the script


```python
import sys
import importlib

tool_path = r"{enter path to Bookit_MayaTool folder}"

if tool_path not in sys.path:
    sys.path.append(tool_path)

from bookit import dev

dev.run()
```

## Features
- Scatter books along a curve
- Randomized placement with seed control
- Rotation alignment to curve
- Live update when curve changes
- Chance to Skip Book (%)
- Preview vs Bake workflow

---

## My Goal
- Automate repetitive placement tasks
- Explore procedural approaches inside Maya using python
- Build a small Maya tool with a focus on clean architecture and maintainable code