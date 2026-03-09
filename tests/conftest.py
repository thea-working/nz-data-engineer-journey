import sys
from pathlib import Path

# 把项目根目录加入 sys.path
ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))