"""Test Supabase Storage URL generation"""
from supabase import create_client
from dotenv import load_dotenv
import os

load_dotenv()

supabase_url = os.getenv('SUPABASE_URL')
supabase_key = os.getenv('SUPABASE_KEY')
supabase = create_client(supabase_url, supabase_key)

BUCKET_NAME = 'scholarship_bucket'

# Get one archived renewal record
renewals = supabase.table('renew').select('*').eq('archived', True).limit(1).execute()

if renewals.data:
    renewal = renewals.data[0]
    print(f"Renewal ID: {renewal['renewal_id']}")
    print(f"Student ID: {renewal['student_id']}")
    print(f"\nCurrent database values:")
    print(f"  school_id_path: {renewal.get('school_id_path')}")
    print(f"  id_picture_path: {renewal.get('id_picture_path')}")
    
    # List what's actually in storage
    print(f"\n\nFiles in Supabase Storage:")
    try:
        files = supabase.storage.from_(BUCKET_NAME).list()
        for f in files:
            print(f"  - {f['name']}")
            # List files inside folders
            if f.get('id'):
                try:
                    subfiles = supabase.storage.from_(BUCKET_NAME).list(f['name'])
                    for sf in subfiles:
                        print(f"    - {f['name']}/{sf['name']}")
                except:
                    pass
    except Exception as e:
        print(f"  Error: {e}")
    
    # Test URL generation
    print(f"\n\nTesting URL generation for student {renewal['student_id']}:")
    test_path = f"{renewal['student_id']}/school_id.jpg"
    test_url = supabase.storage.from_(BUCKET_NAME).get_public_url(test_path)
    print(f"  Generated URL: {test_url}")
    print(f"\n  Copy this URL and paste in browser to test")
else:
    print("No archived renewals found")
