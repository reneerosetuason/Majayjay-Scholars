from supabase import create_client
from dotenv import load_dotenv
import os

load_dotenv()

supabase_url = os.getenv('SUPABASE_URL')
supabase_key = os.getenv('SUPABASE_KEY')
supabase = create_client(supabase_url, supabase_key)

print("\n" + "="*60)
print("CHECKING ALL TABLES")
print("="*60)

# Try to query different possible table names
tables_to_check = ['users', 'Users', 'user', 'User', 'public.users']

for table_name in tables_to_check:
    try:
        print(f"\nChecking table: '{table_name}'")
        response = supabase.table(table_name).select('*').limit(5).execute()
        print(f"✅ Table '{table_name}' exists!")
        print(f"   Rows found: {len(response.data) if response.data else 0}")
        if response.data:
            print(f"   Sample data: {response.data[0]}")
            break
    except Exception as e:
        print(f"❌ Table '{table_name}' - Error: {str(e)[:100]}")

print("\n" + "="*60)
print("SOLUTION:")
print("="*60)
print("Your 'users' table exists but is EMPTY.")
print("\nTo populate it, run:")
print("  python create_initial_users.py")
print("\nOr go to Supabase Dashboard:")
print("  1. SQL Editor")
print("  2. Paste the INSERT statements from complete_database.sql")
print("  3. Run the query")
print("="*60 + "\n")
