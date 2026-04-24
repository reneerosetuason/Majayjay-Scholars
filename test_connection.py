from supabase import create_client, Client
from dotenv import load_dotenv
import os
import sys

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Load environment variables
load_dotenv()

print("="*60)
print("TESTING SUPABASE CONNECTION")
print("="*60)

# Get credentials
supabase_url = os.getenv('SUPABASE_URL')
supabase_key = os.getenv('SUPABASE_KEY')

print(f"\nSupabase URL: {supabase_url}")
print(f"Supabase Key (first 20 chars): {supabase_key[:20] if supabase_key else 'None'}...")
print(f"Supabase Key length: {len(supabase_key) if supabase_key else 0}")

if not supabase_url or not supabase_key:
    print("\n❌ ERROR: Missing Supabase credentials in .env file!")
    exit(1)

try:
    # Create Supabase client
    print("\n[1] Creating Supabase client...")
    supabase: Client = create_client(supabase_url, supabase_key)
    print("✓ Client created successfully")
    
    # Test connection by querying users table
    print("\n[2] Testing connection - querying users table...")
    response = supabase.table('users').select('*').execute()
    print(f"✓ Query successful!")
    print(f"✓ Users found: {len(response.data) if response.data else 0}")
    
    if response.data:
        print("\n[3] Users in database:")
        print("-" * 60)
        for user in response.data:
            print(f"  ID: {user.get('user_id')}")
            print(f"  Email: {user.get('email')}")
            print(f"  Type: {user.get('user_type')}")
            print(f"  Name: {user.get('first_name')} {user.get('last_name')}")
            print(f"  Password: {user.get('password')}")
            print("-" * 60)
    else:
        print("\n⚠️ WARNING: Users table is EMPTY!")
        print("You need to create users in the database.")
        print("\nRun: python create_initial_users.py")
    
    print("\n✓ Connection test PASSED!")
    
except Exception as e:
    print(f"\n❌ ERROR: Connection test FAILED!")
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
