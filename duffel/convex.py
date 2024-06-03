from convex import ConvexClient
import os
from dotenv import load_dotenv

load_dotenv()

client = ConvexClient(os.environ.get("CONVEX_URL"))
