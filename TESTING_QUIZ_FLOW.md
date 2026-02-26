# Testing the Quiz Flow - Debug Guide

## Goal
Test the complete quiz flow (answer quiz → submit → view results) while capturing browser console logs to identify where the results page issue originates.

## Prerequisites
- React dev server running on http://localhost:5174
- Django backend running on http://localhost:8000
- Latest code changes deployed (with enhanced logging)

## Test Steps

### Step 1: Open Browser Developer Tools
1. Open http://localhost:5174 in your browser
2. Press **F12** to open Developer Tools
3. Go to the **Console** tab
4. Make sure "Errors" are visible (check the filter buttons)

### Step 2: Answer the Quiz
1. Click on "Take the Quiz" or navigate to Quiz page
2. You should see all 19 questions on one page
3. Use the sliders to answer each question with different values (don't just use the same value for all):
   - Answer some with high values (8-10) for some questions
   - Answer some with low values (2-4) for others
   - This helps verify ML produces variant outputs
4. Watch the Console for any messages starting with `[Quiz]`

### Step 3: Submit the Quiz
1. Scroll to the bottom of the page
2. Click **"Submit & Get Results"** button
3. **Watch the Console closely** - you should see:
   - `[Quiz] Submitting X answers...`
   - `[Quiz] Session ID: ...`
   - `[Quiz] Calling submitQuiz API...`
   - `[Quiz] Submit response: {...}`
   - `[ML] Calling generateRecommendations API...`
   - `[ML] Full recommendations response: {...}`
   - `[Storage] Payload type: ...`
   - `[Storage] Payload keys: [...]`
   - `[Storage] Has top_recommendations: true`
   - `[Storage] top_recommendations length: 5`
   - `[Storage] About to save to sessionStorage...`
   - `[Storage] Verification - data saved successfully: true`
   - `[Storage] Saved session ID: ...`
   - `[Storage] Saved primary_career: ...`
   - `[Navigation] Navigating to results page...`
   - `[Navigation] ✓ onNavigate called`

### Step 4: Check Results Page
1. After navigating, you should see the Results page with:
   - Career recommendations with compatibility scores
   - Ability scores displayed in charts
   - Primary career prominently displayed
2. In the Console, you should see:
   - `[Results] ===== useEffect STARTED =====`
   - `[Results] Page mounted, attempting to load results...`
   - `[Results] Session ID: ...`
   - `[Results] Checking sessionStorage...`
   - `[Results] sessionStorage.results: FOUND`
   - `[Results] Using sessionStorage data`
   - `[Results] Keys in savedResults: [...]`
   - `[Results] ✓ Valid data from sessionStorage, setting state...`

## Interpreting Results

### ✓ If You See Results Page
1. Note what the primary career recommendation is
2. Check if ability scores are displayed correctly
3. Copy ALL console logs from "[Quiz]", "[ML]", "[Storage]", and "[Results]" sections

### ✗ If You See Blank/Error Page
1. **Look at the Console to identify where the flow stopped:**
   
   - **Stops at "[Quiz]" logs?** → Quiz submission issue
     - Check HTTP status of submitQuiz API call
     - Verify formatOf quiz answers
   
   - **Stops at "[ML]" logs?** → ML recommendation generation issue
     - Check if `generateRecommendations` status is 201
     - Look for error in response (e.g., "No quiz answers found")
   
   - **Stops at "[Storage]" logs?** → Data saving issue
     - Check if "Payload has top_recommendations: true"
     - Check if "data saved successfully: true"
   
   - **Stops at "[Navigation]"?** → Navigation issue
     - Page didn't navigate to results
     - Check if onNavigate function exists
   
   - **Never logging "[Results]"?** → ResultsPage not mounting
     - Component may have mounted but useEffect has an error
     - Check for JavaScript errors in Console

## Key Things to Share

When you run this test, please share:

1. **The browser console logs** - Copy all logs starting with `[Quiz]`, `[ML]`, `[Storage]`, `[Results]`
2. **Any error messages** in red in the console
3. **The point where logging STOPS** - This will tell us exactly where the flow breaks
4. **API response if visible** - The `[ML] Full recommendations response:` log shows what the backend returned

## Example of Successful Flow

```
[Quiz] Submitting 19 answers...
[Quiz] Session ID: session_1771617719727_abc123
[Quiz] Calling submitQuiz API...
[Quiz] Submit response: {success: true, submission_id: '4fc...', ...}
✓ Quiz answers submitted successfully
[ML] Calling generateRecommendations API...
[ML] Full recommendations response: {success: true, primary_career: 'Consultant', top_recommendations: Array(5), abilities: {...}, ...}
[Storage] Payload type: object Is array: false
[Storage] Payload keys: (7) ['success', 'recommendation_id', 'session_id', 'primary_career', 'primary_compatibility', 'top_recommendations', 'abilities']
[Storage] Has top_recommendations: true
[Storage] top_recommendations is array: true
[Storage] top_recommendations length: 5
[Storage] About to save to sessionStorage...
[Storage] Verification - data saved successfully: true
[Storage] Saved session ID: session_1771617719727_abc123
[Storage] Saved primary_career: Consultant
[Navigation] Navigating to results page...
[Navigation] ✓ onNavigate called
[Results] ===== useEffect STARTED =====
[Results] Page mounted, attempting to load results...
[Results] Session ID: session_1771617719727_abc123
[Results] Checking sessionStorage...
[Results] sessionStorage.results: FOUND
[Results] Using sessionStorage data
[Results] Keys in savedResults: (7) ['success', 'recommendation_id', 'session_id', 'primary_career', 'primary_compatibility', 'top_recommendations', 'abilities']
[Results] savedResults.top_recommendations: Array(5) [ {...}, {...}, {...}, {...}, {...} ]
[Results] ✓ Valid data from sessionStorage, setting state...
```

## Troubleshooting Before Testing

1. **Browser cache:**
   - Press Ctrl+Shift+Delete to clear cache
   - Or disable cache in DevTools (Settings → Network → Disable cache while DevTools open)

2. **Ensure frontend is fresh:**
   - Kill the Vite dev server with Ctrl+C
   - Run `npm run dev` in `frontend/` directory
   - Wait for "ready in Xms" message

3. **Ensure backend is running:**
   - Verify `http://localhost:8000/api/quiz/questions/` returns questions
   - Or check Django server terminal (should show no errors)

## Next Steps

After you test and share the console logs, I can pinpoint the exact issue and provide a fix.
