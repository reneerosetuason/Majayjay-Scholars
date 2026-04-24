from supabase import create_client
from dotenv import load_dotenv
import os

load_dotenv()

supabase_url = os.getenv('SUPABASE_URL')
supabase_key = os.getenv('SUPABASE_KEY')
supabase = create_client(supabase_url, supabase_key)

print("\n" + "="*60)
print("ALL USERS IN DATABASE")
print("="*60)

response = supabase.table('users').select('*').execute()

if response.data:
    print(f"\nTotal users: {len(response.data)}\n")
    for user in response.data:
        print(f"📧 Email: {user['email']}")
        print(f"🔑 Password: {user['password']}")
        print(f"👤 User Type: {user['user_type']}")
        print(f"📛 Name: {user.get('first_name', '')} {user.get('last_name', '')}")
        print("-" * 60)
else:
    print("\n❌ No users found!")

print("="*60 + "\n")
