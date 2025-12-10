"""
Migrate local files to Supabase Storage and update database records
"""
from supabase import create_client
from dotenv import load_dotenv
import os
from pathlib import Path

load_dotenv()

supabase_url = os.getenv('SUPABASE_URL')
supabase_key = os.getenv('SUPABASE_KEY')
supabase = create_client(supabase_url, supabase_key)

BUCKET_NAME = 'scholarship_bucket'
LOCAL_UPLOAD_DIR = 'static/uploads'

def upload_file_to_supabase(local_path, storage_path):
    """Upload a local file to Supabase Storage"""
    try:
        with open(local_path, 'rb') as f:
            file_bytes = f.read()
        
        # Determine content type
        ext = local_path.rsplit('.', 1)[-1].lower()
        content_type = 'image/jpeg' if ext in ['jpg', 'jpeg'] else f'image/{ext}'
        
        supabase.storage.from_(BUCKET_NAME).upload(
            path=storage_path,
            file=file_bytes,
            file_options={"content-type": content_type, "upsert": "true"}
        )
        
        public_url = supabase.storage.from_(BUCKET_NAME).get_public_url(storage_path)
        return public_url
    except Exception as e:
        print(f"    ❌ Error uploading: {e}")
        return None

def migrate_records():
    """Migrate all old records to Supabase Storage"""
    print("="*60)
    print("MIGRATING LOCAL FILES TO SUPABASE STORAGE")
    print("="*60)
    
    # Get all records with old filenames
    apps = supabase.table('application').select('*').execute()
    renewals = supabase.table('renew').select('*').execute()
    
    migrated_count = 0
    failed_count = 0
    
    # Process applications
    for app in apps.data:
        if not app.get('school_id_path') or app['school_id_path'].startswith('https://'):
            continue  # Skip if already migrated
        
        print(f"\n📄 Application {app['application_id']} - Student: {app['student_id']}")
        student_id = app['student_id']
        updates = {}
        
        for field in ['school_id', 'id_picture', 'birth_certificate', 'grades', 'cor']:
            path_field = f"{field}_path"
            old_filename = app.get(path_field)
            
            if not old_filename or old_filename.startswith('https://'):
                continue
            
            local_file = os.path.join(LOCAL_UPLOAD_DIR, old_filename)
            
            if os.path.exists(local_file):
                ext = old_filename.rsplit('.', 1)[-1]
                storage_path = f"{student_id}/{field}.{ext}"
                
                print(f"  📤 Uploading {field}...")
                public_url = upload_file_to_supabase(local_file, storage_path)
                
                if public_url:
                    updates[path_field] = public_url
                    print(f"    ✅ {public_url}")
                else:
                    failed_count += 1
            else:
                print(f"  ⚠️  File not found: {old_filename}")
                failed_count += 1
        
        if updates:
            supabase.table('application').update(updates).eq('application_id', app['application_id']).execute()
            migrated_count += 1
    
    # Process renewals
    for renewal in renewals.data:
        if not renewal.get('school_id_path') or renewal['school_id_path'].startswith('https://'):
            continue
        
        archived = " (ARCHIVED)" if renewal.get('archived') else ""
        print(f"\n🔄 Renewal {renewal['renewal_id']}{archived} - Student: {renewal['student_id']}")
        student_id = renewal['student_id']
        updates = {}
        
        for field in ['school_id', 'id_picture', 'birth_certificate', 'grades', 'cor']:
            path_field = f"{field}_path"
            old_filename = renewal.get(path_field)
            
            if not old_filename or old_filename.startswith('https://'):
                continue
            
            local_file = os.path.join(LOCAL_UPLOAD_DIR, old_filename)
            
            if os.path.exists(local_file):
                ext = old_filename.rsplit('.', 1)[-1]
                storage_path = f"{student_id}/{field}.{ext}"
                
                print(f"  📤 Uploading {field}...")
                public_url = upload_file_to_supabase(local_file, storage_path)
                
                if public_url:
                    updates[path_field] = public_url
                    print(f"    ✅ {public_url}")
                else:
                    failed_count += 1
            else:
                print(f"  ⚠️  File not found: {old_filename}")
                failed_count += 1
        
        if updates:
            supabase.table('renew').update(updates).eq('renewal_id', renewal['renewal_id']).execute()
            migrated_count += 1
    
    print("\n" + "="*60)
    print(f"✅ MIGRATION COMPLETE")
    print(f"   Records migrated: {migrated_count}")
    print(f"   Files failed: {failed_count}")
    print("="*60)

if __name__ == '__main__':
    print("\n⚠️  This will upload local files to Supabase Storage")
    print("   and update database records with new URLs.\n")
    
    response = input("Continue? (yes/no): ").strip().lower()
    if response == 'yes':
        migrate_records()
        print("\n✅ Done! Check your mayor records page - files should now work.")
    else:
        print("\n❌ Cancelled.")
