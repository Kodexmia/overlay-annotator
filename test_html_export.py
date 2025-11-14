#!/usr/bin/env python3
"""
Test HTML generation with your actual session data
"""
import sys
from pathlib import Path

# Add app to path
sys.path.insert(0, str(Path(__file__).parent))

from app.core.storage import SessionStore

def test_html_generation(session_path):
    """Test HTML export with existing session"""
    
    print(f"Testing HTML generation for: {session_path}")
    print("=" * 60)
    
    # Load session
    store = SessionStore(session_path)
    
    # Check templates exist
    print("\n1. Checking templates...")
    md_template = store.tpl_dir / "report.md.j2"
    html_template = store.tpl_dir / "report.html.j2"
    
    print(f"   MD template: {md_template.exists()} - {md_template}")
    print(f"   HTML template: {html_template.exists()} - {html_template}")
    
    if not html_template.exists():
        print("   ❌ HTML template missing! Creating it...")
        from app.core.storage import SessionStore
        # Re-init will create template
        store = SessionStore(session_path)
        print(f"   ✓ Template created: {html_template.exists()}")
    
    # Load entries
    print("\n2. Loading entries...")
    entries = store.load_entries()
    print(f"   Found {len(entries)} entries")
    
    for i, entry in enumerate(entries, 1):
        print(f"   {i}. {entry.title[:50]}")
        print(f"      Image: {entry.image.path}")
        img_full_path = store.root / entry.image.path
        print(f"      Exists: {img_full_path.exists()}")
    
    # Test Markdown export
    print("\n3. Testing Markdown export...")
    try:
        md_path = store.export_markdown()
        print(f"   ✓ MD exported: {md_path}")
        print(f"   Size: {md_path.stat().st_size} bytes")
    except Exception as e:
        print(f"   ❌ MD export failed: {e}")
        return False
    
    # Test HTML export
    print("\n4. Testing HTML export...")
    try:
        html_path = store.export_html()
        print(f"   ✓ HTML exported: {html_path}")
        print(f"   Size: {html_path.stat().st_size} bytes")
        
        # Check HTML content
        html_content = html_path.read_text(encoding='utf-8')
        print(f"   HTML length: {len(html_content)} characters")
        
        # Check for embedded images
        base64_count = html_content.count('data:image/jpeg;base64,')
        print(f"   Embedded images: {base64_count}")
        
        if base64_count != len(entries):
            print(f"   ⚠️  Warning: Expected {len(entries)} images, found {base64_count}")
        
        # Show first 500 chars
        print("\n5. HTML Preview (first 500 chars):")
        print("   " + "-" * 50)
        print("   " + html_content[:500].replace('\n', '\n   '))
        print("   " + "-" * 50)
        
        print(f"\n✅ SUCCESS! HTML report generated at:")
        print(f"   {html_path.absolute()}")
        print(f"\nOpen in browser:")
        print(f"   file:///{html_path.absolute()}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ HTML export failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test_html_export.py <session_path>")
        print("\nExample:")
        print("  python test_html_export.py sessions/my-session")
        sys.exit(1)
    
    session_path = Path(sys.argv[1])
    
    if not session_path.exists():
        print(f"❌ Session path not found: {session_path}")
        sys.exit(1)
    
    success = test_html_generation(session_path)
    sys.exit(0 if success else 1)
