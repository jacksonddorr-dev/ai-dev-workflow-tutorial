import sys
from pathlib import Path

# Add the parent directory to the path so pytest can find data_loader
sys.path.insert(0, str(Path(__file__).parent.parent))
