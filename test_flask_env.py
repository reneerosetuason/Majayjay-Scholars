import os
from dotenv import load_dotenv

print("="*60)
print("TESTING FLASK ENVIRONMENT VARIABLES")
print("="*60)

# Load environment variables
load_dotenv()

print(f"\nCurrent working directory: {os.getcwd()}")
print(f"\n.env file location: {os.path.join(os.getcwd(), '.env')}")
print(f".env file exists: {os.path.exists('.env')}")

print(f"\nEnvironment variables:")
print(f"  SUPABASE_URL: {os.getenv('SUPABASE_URL')}")
print(f"  SUPABASE_KEY (first 20): {os.getenv('SUPABASE_KEY')[:20] if os.getenv('SUPABASE_KEY') else 'None'}...")
print(f"  SECRET_KEY: {os.getenv('SECRET_KEY')}")
print(f"  SENDER_EMAIL: {os.getenv('SENDER_EMAIL')}")

if os.getenv('SUPABASE_URL') and os.getenv('SUPABASE_KEY'):
    print("\n✓ Environment variables loaded successfully!")
else:
    print("\n❌ ERROR: Environment variables not loaded!")
