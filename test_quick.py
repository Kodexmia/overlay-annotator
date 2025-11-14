#!/usr/bin/env python3
"""
Quick test script for Overlay Annotator
"""
import sys
from pathlib import Path

# Add app to path
sys.path.insert(0, str(Path(__file__).parent / "app"))

def test_imports():
    """Test that all modules can be imported"""
    print("Testing imports...")
    
    try:
        from app.ui.main_window import MainWindow
        print("✓ main_window")
        
        from app.ui.capture_overlay import CaptureOverlay
        print("✓ capture_overlay")
        
        from app.ui.annotation_canvas import AnnotationCanvas, ToolType
        print("✓ annotation_canvas")
        
        from app.ui.annotation_toolbar import AnnotationToolbar
        print("✓ annotation_toolbar")
        
        from app.core.models import Entry, ImageModel
        print("✓ models")
        
        from app.core.storage import SessionStore
        print("✓ storage")
        
        print("\n✅ All imports successful!")
        return True
        
    except Exception as e:
        print(f"\n❌ Import failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_session_storage():
    """Test session storage"""
    print("\nTesting session storage...")
    
    try:
        from app.core.storage import SessionStore
        from app.core.models import Entry, ImageModel
        from PIL import Image
        import tempfile
        
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create store
            store = SessionStore(Path(tmpdir))
            print("✓ Created session store")
            
            # Save test image
            img = Image.new("RGB", (100, 100), color="red")
            img_path = store.save_image(img)
            print(f"✓ Saved image: {img_path}")
            
            # Create entry
            entry = Entry.new(
                title="Test Entry",
                notes="Test notes",
                layout="image-left",
                image=ImageModel(
                    path=str(img_path),
                    width=100,
                    height=100
                )
            )
            store.save_entry(entry)
            print(f"✓ Saved entry: {entry.id}")
            
            # Load entries
            entries = store.load_entries()
            assert len(entries) == 1
            assert entries[0].title == "Test Entry"
            print("✓ Loaded entries")
            
            print("\n✅ Session storage tests passed!")
            return True
            
    except Exception as e:
        print(f"\n❌ Storage test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("Overlay Annotator - Quick Tests")
    print("=" * 50)
    
    success = True
    success = test_imports() and success
    success = test_session_storage() and success
    
    print("\n" + "=" * 50)
    if success:
        print("✅ ALL TESTS PASSED")
        print("\nReady to run! Execute:")
        print("  python -m app.main")
    else:
        print("❌ SOME TESTS FAILED")
        sys.exit(1)
    print("=" * 50)
