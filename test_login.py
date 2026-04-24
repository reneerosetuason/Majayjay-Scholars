from supabase import create_client, Client
from dotenv import load_dotenv
import os
import sys

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Load environment variables
load_dotenv()

supabase_url = os.getenv('SUPABASE_URL')
supabase_key = os.getenv('SUPABASE_KEY')
supabase: Client = create_client(supabase_url, supabase_key)

print("="*60)
print("TESTING LOGIN LOGIC")
print("="*60)

# Test with mayor credentials
test_email = "mayor@gmail.com"
test_password = "asdfgh"

print(f"\nAttempting login with:")
print(f"  Email: '{test_email}'")
print(f"  Password: '{test_password}'")

try:
    print(f"\n[1] Querying database for email: {test_email}")
    response = supabase.table('users').select('*').eq('email', test_email).execute()
    
    print(f"[2] Query response:")
    print(f"  Data: {response.data}")
    print(f"  Users found: {len(response.data) if response.data else 0}")
    
    if response.data and len(response.data) > 0:
        user = response.data[0]
        print(f"\n[3] User found:")
        print(f"  user_id: {user['user_id']}")
        print(f"  email: {user['email']}")
        print(f"  user_type: {user['user_type']}")
        print(f"  first_name: {user['first_name']}")
        print(f"  last_name: {user['last_name']}")
        print(f"  password (raw): {repr(user['password'])}")
        print(f"  password (type): {type(user['password'])}")
        
        print(f"\n[4] Password comparison:")
        print(f"  Stored password: '{user['password']}'")
        print(f"  Entered password: '{test_password}'")
        print(f"  Stored == Entered: {user['password'] == test_password}")
        print(f"  Stored length: {len(user['password']) if user['password'] else 0}")
        print(f"  Entered length: {len(test_password)}")
        
        if user['password'] == test_password:
            print(f"\n✓ LOGIN SUCCESSFUL!")
            print(f"  Would redirect to: mayor_dashboard")
        else:
            print(f"\n❌ LOGIN FAILED - Password mismatch!")
            print(f"  Checking for whitespace issues...")
            print(f"  Stored (stripped): '{user['password'].strip() if user['password'] else ''}'")
            print(f"  Match after strip: {user['password'].strip() == test_password if user['password'] else False}")
    else:
        print(f"\n❌ No user found with email: {test_email}")
        
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
