import os
from dotenv import load_dotenv
load_dotenv()

AGENT_LOOP_SECONDS      = int(os.getenv("AGENT_LOOP_SECONDS", 5))
TICKER                  = os.getenv("TICKER")