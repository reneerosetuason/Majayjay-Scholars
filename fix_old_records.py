"""
Script to fix old database records that have filenames instead of full Supabase URLs
"""
from supabase import create_client
from dotenv import load_dotenv
import os

load_dotenv()

supabase_url = os.getenv('SUPABASE_URL')
supabase_key = os.getenv('SUPABASE_KEY')
supabase = create_client(supabase_url, supabase_key)

BUCKET_NAME = 'scholarship_bucket'

def list_storage_files():
    """List all files in Supabase Storage bucket"""
    try:
        files = supabase.storage.from_(BUCKET_NAME).list()
        print(f"\n{'='*60}")
        print(f"FILES IN SUPABASE STORAGE BUCKET: {BUCKET_NAME}")
        print(f"{'='*60}")
        for file in files:
            print(f"  - {file['name']}")
        return files
    except Exception as e:
        print(f"Error listing storage files: {e}")
        return []

def check_old_records():
    """Check for records with old filename format (not full URLs)"""
    print(f"\n{'='*60}")
    print("CHECKING FOR OLD RECORDS IN DATABASE")
    print(f"{'='*60}")
    
    # Check application table
    apps = supabase.table('application').select('application_id, student_id, school_id_path, id_picture_path, birth_certificate_path, grades_path, cor_path').execute()
    
    old_apps = []
    for app in apps.data:
        # Check if any path doesn't start with https://
        for field in ['school_id_path', 'id_picture_path', 'birth_certificate_path', 'grades_path', 'cor_path']:
            if app.get(field) and not app[field].startswith('https://'):
                old_apps.append(app)
                break
    
    print(f"\nAPPLICATIONS TABLE:")
    print(f"  Total records: {len(apps.data)}")
    print(f"  Old format (needs fixing): {len(old_apps)}")
    
    if old_apps:
        print(f"\n  Sample old records:")
        for app in old_apps[:3]:
            print(f"    - App ID {app['application_id']}, Student ID: {app['student_id']}")
            print(f"      school_id_path: {app.get('school_id_path')}")
    
    # Check renew table
    renewals = supabase.table('renew').select('renewal_id, student_id, school_id_path, id_picture_path, birth_certificate_path, grades_path, cor_path, archived').execute()
    
    old_renewals = []
    for renewal in renewals.data:
        for field in ['school_id_path', 'id_picture_path', 'birth_certificate_path', 'grades_path', 'cor_path']:
            if renewal.get(field) and not renewal[field].startswith('https://'):
                old_renewals.append(renewal)
                break
    
    print(f"\nRENEW TABLE:")
    print(f"  Total records: {len(renewals.data)}")
    print(f"  Old format (needs fixing): {len(old_renewals)}")
    
    if old_renewals:
        print(f"\n  Sample old renewal records:")
        for renewal in old_renewals[:3]:
            archived_status = " (ARCHIVED)" if renewal.get('archived') else ""
            print(f"    - Renewal ID {renewal['renewal_id']}, Student ID: {renewal['student_id']}{archived_status}")
            print(f"      school_id_path: {renewal.get('school_id_path')}")
    
    return old_apps, old_renewals

def fix_records(old_apps, old_renewals, dry_run=True):
    """Fix old records by converting filenames to full Supabase URLs"""
    print(f"\n{'='*60}")
    print(f"{'DRY RUN - NO CHANGES WILL BE MADE' if dry_run else 'FIXING RECORDS'}")
    print(f"{'='*60}")
    
    fixed_count = 0
    
    # Fix applications
    for app in old_apps:
        student_id = app['student_id']
        updates = {}
        
        for field in ['school_id', 'id_picture', 'birth_certificate', 'grades', 'cor']:
            path_field = f"{field}_path"
            old_value = app.get(path_field)
            
            if old_value and not old_value.startswith('https://'):
                # Extract extension from old filename
                ext = old_value.rsplit('.', 1)[-1] if '.' in old_value else 'jpg'
                # Build new Supabase URL
                file_path = f"{student_id}/{field}.{ext}"
                new_url = supabase.storage.from_(BUCKET_NAME).get_public_url(file_path)
                updates[path_field] = new_url
                
                print(f"\n  App {app['application_id']} - {field}:")
                print(f"    OLD: {old_value}")
                print(f"    NEW: {new_url}")
        
        if updates and not dry_run:
            supabase.table('application').update(updates).eq('application_id', app['application_id']).execute()
            fixed_count += 1
    
    # Fix renewals
    for renewal in old_renewals:
        student_id = renewal['student_id']
        updates = {}
        
        for field in ['school_id', 'id_picture', 'birth_certificate', 'grades', 'cor']:
            path_field = f"{field}_path"
            old_value = renewal.get(path_field)
            
            if old_value and not old_value.startswith('https://'):
                ext = old_value.rsplit('.', 1)[-1] if '.' in old_value else 'jpg'
                file_path = f"{student_id}/{field}.{ext}"
                new_url = supabase.storage.from_(BUCKET_NAME).get_public_url(file_path)
                updates[path_field] = new_url
                
                archived_status = " (ARCHIVED)" if renewal.get('archived') else ""
                print(f"\n  Renewal {renewal['renewal_id']}{archived_status} - {field}:")
                print(f"    OLD: {old_value}")
                print(f"    NEW: {new_url}")
        
        if updates and not dry_run:
            supabase.table('renew').update(updates).eq('renewal_id', renewal['renewal_id']).execute()
            fixed_count += 1
    
    if dry_run:
        print(f"\n{'='*60}")
        print(f"DRY RUN COMPLETE - No changes made")
        print(f"Run with dry_run=False to apply changes")
        print(f"{'='*60}")
    else:
        print(f"\n{'='*60}")
        print(f"✅ FIXED {fixed_count} RECORDS")
        print(f"{'='*60}")

if __name__ == '__main__':
    print("SUPABASE STORAGE & DATABASE DIAGNOSTIC TOOL")
    
    # Step 1: List storage files
    storage_files = list_storage_files()
    
    # Step 2: Check for old records
    old_apps, old_renewals = check_old_records()
    
    # Step 3: Fix records (dry run first)
    if old_apps or old_renewals:
        print("\n" + "="*60)
        print("READY TO FIX RECORDS")
        print("="*60)
        print("\nThis will update database records to use full Supabase URLs.")
        print("First, let's do a DRY RUN to see what would change...\n")
        
        fix_records(old_apps, old_renewals, dry_run=True)
        
        print("\n" + "="*60)
        response = input("\nDo you want to APPLY these changes? (yes/no): ").strip().lower()
        if response == 'yes':
            fix_records(old_apps, old_renewals, dry_run=False)
            print("\n✅ All done! Your records should now work correctly.")
        else:
            print("\n❌ Cancelled. No changes were made.")
    else:
        print("\n✅ No old records found! All records are already using full Supabase URLs.")
