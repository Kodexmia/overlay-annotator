# Overlay Annotator V3.3 - Stability & Testing Guide

**Focus:** Fix bugs, ensure stability, verify all features work

---

## ✅ **TESTING CHECKLIST**

### **1. Basic Functionality**

#### **Capture:**
- [ ] Ctrl+Alt+S triggers overlay
- [ ] Capture button triggers overlay
- [ ] Can select region
- [ ] Image loads in canvas
- [ ] Toolbar appears after capture

#### **Annotation Tools:**
- [ ] Arrow tool works (draws arrow)
- [ ] Box tool works (draws rectangle outline)
- [ ] Pen tool works (draws freehand line)
- [ ] Blur tool works (blurs region)
- [ ] Text tool works (prompts for text, places it)

#### **Text Tool Specifically:**
- [ ] Click "T" button
- [ ] Click on canvas
- [ ] Dialog appears asking for text
- [ ] Enter text
- [ ] Text appears at click position
- [ ] Can add multiple text annotations
- [ ] Text saves with entry

#### **Saving:**
- [ ] Can add title
- [ ] Can add notes
- [ ] Click "Save Entry"
- [ ] Entry appears in left panel list
- [ ] Entry saved to disk (check metadata folder)

#### **Export:**
- [ ] Click "Export Report"
- [ ] Markdown generated (report.md)
- [ ] HTML generated (report.html)
- [ ] Dialog asks to open HTML
- [ ] HTML opens in browser correctly
- [ ] All images embedded in HTML

---

## 🐛 **KNOWN ISSUES TO FIX**

### **Issue 1: Text Tool Dialog Not Appearing**

**Symptom:** Click T, click canvas, nothing happens

**Fix Location:** `app/ui/main_window.py`

**Check:**
```python
# Verify toolbar signal is connected
self.annotation_toolbar.text_requested.connect(self.canvas.add_text_annotation)
```

**Test:**
1. Run app
2. Capture screenshot
3. Click "T" button (should highlight)
4. Click on canvas
5. Dialog should appear: "Enter text:"
6. Type text, click OK
7. Text should appear on canvas

---

### **Issue 2: HTML Export Template Missing**

**Symptom:** Export fails with "template not found"

**Fix Location:** `app/core/storage.py`

**Already Fixed in V3.2.2** ✓

**Verify:**
1. Create new session
2. Check `sessions/your-session/_templates/`
3. Should contain:
   - report.md.j2 ✓
   - report.html.j2 ✓

---

### **Issue 3: Rectangle Fills After Arrow**

**Symptom:** Draw arrow, then box → box is filled

**Fix Location:** `app/ui/annotation_canvas.py`

**Already Fixed in V3.2.1** ✓

**Test:**
1. Draw an arrow
2. Switch to box tool
3. Draw a rectangle
4. Should be OUTLINE only, not filled

---

### **Issue 4: Rectangle Drawing Direction**

**Symptom:** Draw bottom-right to top-left → crash

**Fix Location:** `app/ui/annotation_canvas.py`

**Already Fixed in V3.2.1** ✓

**Test:**
1. Select box tool
2. Click bottom-right, drag to top-left
3. Should draw correctly without crash

---

### **Issue 5: Toolbar Stays Floating**

**Symptom:** Toolbar doesn't close after save

**Current Behavior:** Closes after "Save Entry" ✓

**Test:**
1. Capture and annotate
2. Click "Save Entry"
3. Toolbar should hide automatically

**Enhancement Request:**
- Add "X" button to manually close
- Add hotkey to toggle (Esc?)
- Add option to dock toolbar

---

## 🔧 **GUI IMPROVEMENTS FOR V3.3**

### **1. Entry List Display**

**Current Issue:** Long titles clutter the list

**Fix:**
```python
# Truncate titles in display
display_text = f"{entry.id[:8]} — {entry.title[:40]}"
if len(entry.title) > 40:
    display_text += "..."
self.entry_list.addItem(display_text)
```

**Location:** `app/ui/main_window.py` line ~209

---

### **2. Status Messages**

**Current Issue:** Some actions don't give feedback

**Add status messages for:**
- [ ] Session loaded: "Loaded N entries"
- [ ] Entry saved: "Entry 'Title' saved"
- [ ] Export started: "Generating report..."
- [ ] Export complete: "Report exported successfully"
- [ ] Capture ready: "Select region to capture"

**Location:** `app/ui/main_window.py`

**Method:** `self.update_status("Message here")`

---

### **3. Error Dialogs**

**Current Issue:** Technical error messages shown to user

**Improve:**
```python
try:
    # operation
except Exception as e:
    if self.logger:
        self.logger.error("Technical details", exc_info=True)
    
    # User-friendly message
    QMessageBox.warning(
        self,
        "Operation Failed",
        "Could not complete operation. Check the log file for details."
    )
```

---

## 🧪 **STEP-BY-STEP TESTING PROCEDURE**

### **Test 1: Fresh Install**

```bash
1. Extract overlay_annotator_v3.2.2.zip
2. pip install -r requirements.txt
3. python -m app.main
4. Expected: App opens, no errors
```

### **Test 2: Create Session**

```bash
1. Click "New Session"
2. Create folder: test_session
3. Expected: Session loaded, _templates created
4. Verify: Check sessions/test_session/_templates/
5. Should have: report.md.j2, report.html.j2
```

### **Test 3: Capture & Annotate**

```bash
1. Click "Capture" or Ctrl+Alt+S
2. Select region of screen
3. Expected: Overlay appears, image loads
4. Click each tool:
   - Arrow: Draw arrow ✓
   - Box: Draw rectangle ✓
   - Pen: Draw freehand ✓
   - Blur: Blur region ✓
   - Text: Click, enter text ✓
5. All should work without crashes
```

### **Test 4: Save Entry**

```bash
1. Add title: "Test Entry"
2. Add notes: "This is a test annotation"
3. Click "Save Entry"
4. Expected:
   - Entry appears in left list
   - Toolbar closes
   - Status: "Entry saved: Test Entry"
5. Verify disk:
   - Check sessions/test_session/images/
   - Check sessions/test_session/metadata/
   - Files should exist
```

### **Test 5: Export Report**

```bash
1. Create 2-3 entries
2. Click "Export Report"
3. Expected:
   - Dialog: "Reports exported successfully!"
   - Shows paths to MD and HTML
   - Asks: "Open HTML report in browser?"
4. Click "Yes"
5. Expected:
   - HTML opens in default browser
   - All images visible (embedded)
   - Beautiful formatting
   - No broken images
```

### **Test 6: Load Existing Session**

```bash
1. Close app
2. Reopen: python -m app.main
3. Click "New Session"
4. Select test_session folder
5. Expected:
   - All entries appear in left list
   - Click entry → loads in canvas
   - Can view all previous work
```

### **Test 7: Text Tool Specifically**

```bash
1. Capture screenshot
2. Click "T" button (text tool)
3. Click anywhere on canvas
4. Expected: Dialog "Enter text:"
5. Type: "This is a test"
6. Click OK
7. Expected: Text appears at click position
8. Repeat: Add another text annotation
9. Save entry
10. Reload entry
11. Expected: All text annotations preserved
```

---

## 🔍 **DEBUGGING GUIDE**

### **If Text Tool Doesn't Work:**

**Check 1: Signal Connection**
```python
# In main_window.py, look for:
self.annotation_toolbar.text_requested.connect(...)
# Should connect to canvas.add_text_annotation
```

**Check 2: Dialog Appears**
```python
# In annotation_toolbar.py, find select_tool method
# When TEXT is clicked, should emit text_requested
```

**Check 3: Console Output**
```bash
# Run with verbose logging
python -m app.main

# Look for:
# - "Text tool selected"
# - "Text position clicked"
# - "Text dialog shown"
```

### **If HTML Export Fails:**

**Check 1: Template Exists**
```bash
ls sessions/your-session/_templates/
# Should show:
# report.md.j2
# report.html.j2
```

**Check 2: Image Paths**
```python
# In metadata/*.json, check:
"image": {
  "path": "images\\entry_20251101_210852.jpg"  # Windows
  # or
  "path": "images/entry_20251101_210852.jpg"   # Linux/Mac
}
```

**Check 3: Log File**
```bash
# Check: ~/overlay_annotator_logs/
# Look for export errors
```

### **If Toolbar Doesn't Appear:**

**Check 1: Toolbar Creation**
```python
# In main_window.py
self.annotation_toolbar = AnnotationToolbar(parent=self)
# parent=self is CRITICAL!
```

**Check 2: Show Call**
```python
# After image loads
self.annotation_toolbar.show()
self.annotation_toolbar.raise_()
```

---

## 📋 **MANUAL TEST RESULTS FORM**

Fill this out after testing:

```
Date: _____________
Tester: _____________
Version: v3.2.2

Test Results:
[ ] Fresh install works
[ ] Session creation works
[ ] Capture button works
[ ] Hotkey Ctrl+Alt+S works
[ ] Arrow tool works
[ ] Box tool works
[ ] Pen tool works
[ ] Blur tool works
[ ] Text tool works ← CRITICAL
[ ] Save entry works
[ ] Entry list shows entries
[ ] Load entry works
[ ] Export MD works
[ ] Export HTML works ← CRITICAL
[ ] HTML opens in browser
[ ] Images embedded in HTML

Bugs Found:
1. _________________________________
2. _________________________________
3. _________________________________

Overall Status: PASS / FAIL
```

---

## 🚀 **V3.3 RELEASE CRITERIA**

**All must pass before release:**

✅ **Core Features:**
- [ ] All annotation tools work
- [ ] Text tool specifically verified
- [ ] Save/load works reliably
- [ ] Export works (both MD and HTML)
- [ ] HTML has embedded images

✅ **Stability:**
- [ ] No crashes during normal use
- [ ] No errors in log during test
- [ ] Works on fresh install
- [ ] Works with existing sessions

✅ **User Experience:**
- [ ] Status messages clear
- [ ] Error messages helpful
- [ ] Toolbar behavior predictable
- [ ] Entry list readable

---

## 📝 **NEXT STEPS**

1. **Run full test suite** (above checklist)
2. **Fix any bugs found**
3. **Verify text tool works**
4. **Verify HTML export works**
5. **Update version to V3.3**
6. **Create release**

---

## 🎯 **FOCUS AREAS**

Based on your feedback:

**Priority 1:** Text tool working ✏️  
**Priority 2:** HTML export verified 🌐  
**Priority 3:** GUI polish 🎨  
**Priority 4:** Stability testing 🧪  

---

**Let's make V3.3 rock-solid!** 🚀
