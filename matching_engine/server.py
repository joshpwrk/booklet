import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Engine import Engine

if __name__ == "__main__":
    engine = Engine(max_counterparties=10)
    engine.consume_queue()