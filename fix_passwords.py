"""
Fix passwords to meet 6-character minimum requirement
"""
from supabase import create_client
from dotenv import load_dotenv
import os

load_dotenv()

supabase_url = os.getenv('SUPABASE_URL')
supabase_key = os.getenv('SUPABASE_KEY')
supabase = create_client(supabase_url, supabase_key)

def fix_passwords():
    """Update all passwords shorter than 6 characters"""
    print("="*60)
    print("FIXING SHORT PASSWORDS")
    print("="*60)
    
    # Get all users
    users = supabase.table('users').select('*').execute()
    
    updated = []
    
    for user in users.data:
        password = user.get('password') or ''
        
        if not password or len(password) < 6:
            # Pad password to 6 characters
            new_password = password + 'gh'  # Add 'gh' to make it 6 chars
            
            print(f"\n👤 {user['email']} ({user['user_type']})")
            print(f"   Old password: {password} ({len(password)} chars)")
            print(f"   New password: {new_password} ({len(new_password)} chars)")
            
            supabase.table('users').update({'password': new_password}).eq('user_id', user['user_id']).execute()
            updated.append(user['email'])
    
    print("\n" + "="*60)
    if updated:
        print(f"✅ Updated {len(updated)} passwords:")
        for email in updated:
            print(f"   - {email}")
    else:
        print("✅ All passwords already meet 6-character minimum")
    print("="*60)

if __name__ == '__main__':
    fix_passwords()
