# Task Submission Workflow Documentation

## Overview
The task submission feature has been enhanced to show submission status, allow edits, and provide a clear review workflow.

## Features Implemented

### 1. **Submission Status Tracking**
Students can now see the status of their submissions:
- 🟡 **Draft** - Submission saved but not submitted
- 🟠 **Pending Review** / **Under Review** - Submitted and waiting for mentor approval
- 🟢 **Approved** - Mentor has approved the submission
- 🔴 **Rejected** - Mentor has rejected with feedback

### 2. **Submissions History**
- Displays the 5 most recent submissions
- Highlights the most recent submission with a special badge🏆
- Shows submission details: title, description, platform, completion date, duration
- Displays current status with color-coded badges
- Shows mentor feedback if available

### 3. **Edit Functionality**
Students can edit submissions that are:
- In **Draft** status
- **Rejected** by mentor (to fix issues and resubmit)

**How to Edit:**
1. Navigate to CLT or SCD page
2. Find your submission in the submissions list
3. Click the "Edit" button (only appears for editable submissions)
4. Update the submission details
5. Re-submit for review

### 4. **Auto-Clear After Review (Mentor Side)** ⭐ NEW
When mentors approve or reject submissions:
- ✅ **Instantly removed** from the pending review list
- 📊 Stats update automatically (pending count decreases)
- 🎯 Keeps the review queue clean and focused
- 📜 History can be viewed by changing the status filter

Benefits:
- No manual refresh needed
- Clear visual feedback that action was taken
- Prevents double-review of the same submission
- Faster workflow for mentors reviewing multiple submissions

### 5. **Status-Based UI**
- **Most Recent Submission**: Highlighted with gradient background and special badge
- **Status Badges**: Color-coded icons showing current state
- **Mentor Feedback**: Displayed in a distinct box when available
- **Edit Button**: Only shown for draft/rejected submissions

## User Workflow

### For Students

#### CLT (Creative Learning Track)
1. **View Submissions**: When you visit the CLT page, you'll see your recent submissions first
2. **Check Status**: Each submission shows its current review status
3. **New Submission**: Click "New Submission" button to create a new entry
4. **Edit Rejected**: If mentor rejected, click "Edit" to revise and resubmit
5. **Track Progress**: View all your submissions and their approval status

#### SCD (Self-Coding Development - LeetCode)
1. **Sync Profile**: Sync your LeetCode stats
2. **View History**: See all your previous profile submissions
3. **Check Approval**: Each sync creates a submission that needs mentor approval
4. **Monitor Status**: Track which submissions are pending, approved, or rejected
5. **Mentor Feedback**: Read mentor comments on your progress

### For Mentors
1. **Review Submissions**: Access submissions through mentor dashboard
2. **See Pending Only**: By default, only pending submissions are shown
3. **Approve/Reject**: Make a decision on student submissions
4. **Provide Feedback**: Add comments explaining approval or requesting changes
5. **Auto-Clear**: Approved/rejected submissions are automatically removed from the review list
6. **View History**: Select "Approved (History)" or "Rejected (History)" to see past reviews
7. **Track Student Progress**: Monitor submission history and improvement

## Mentor Review Workflow

### Default View
- Mentors see **only pending submissions** by default
- This ensures a clean, focused review queue
- Approved and rejected submissions are automatically removed from the main list

### After Approval/Rejection
1. ✅ Submission is reviewed (approved or rejected)
2. 🗑️ **Automatically removed** from the pending list
3. 📊 Stats are updated in real-time
4. 📧 Student can see the updated status in their submissions list
5. 🔄 If rejected, student can edit and resubmit (goes back to pending)

### Viewing History
Mentors can view previously reviewed submissions by:
- Selecting **"Approved (History)"** from the status filter
- Selecting **"Rejected (History)"** from the status filter
- This allows tracking of past decisions without cluttering the review queue

## Technical Details

### Backend Models

#### CLT Submission Status
```python
STATUS_CHOICES = [
    ('draft', 'Draft'),
    ('submitted', 'Submitted'),
    ('under_review', 'Under Review'),
    ('approved', 'Approved'),
    ('rejected', 'Rejected'),
]
```

#### SCD LeetCode Profile Status
```python
STATUS_CHOICES = [
    ('draft', 'Draft'),
    ('pending', 'Pending Review'),
    ('approved', 'Approved'),
    ('rejected', 'Rejected'),
]
```

### API Endpoints

#### CLT Service
- `GET /api/clt/submissions/` - Get all submissions
- `POST /api/clt/submissions/` - Create new submission
- `PATCH /api/clt/submissions/{id}/` - Update submission
- `POST /api/clt/submissions/{id}/submit/` - Submit for review
- `DELETE /api/clt/submissions/{id}/` - Delete draft/rejected submission

#### SCD Service
- `GET /api/scd/profiles/` - Get all LeetCode profiles
- `POST /api/scd/sync/` - Sync LeetCode profile

### UI Components Updated
- `/src/pages/student/CLT.jsx`: Enhanced with submission history and edit functionality
- `/src/pages/student/SCD.jsx`: Added profile history with status tracking
- `/src/pages/mentor/SubmissionReview.jsx`: **Auto-clear approved/rejected submissions**
- `/src/pages/mentor/PillarReview.jsx`: **Auto-clear approved/rejected submissions**
- `/src/services/clt.js`: Includes update and submit methods

### Auto-Clear Implementation

#### Mentor Pages
Both `SubmissionReview.jsx` and `PillarReview.jsx` now implement:

1. **Smart Filtering**
   ```javascript
   // Only show submissions that need review
   const needsReviewStatuses = ['pending', 'submitted', 'under_review', 'draft', 'resubmit'];
   const needsReview = needsReviewStatuses.includes(submission.status);
   ```

2. **Immediate Removal After Review**
   ```javascript
   // Remove from local state instantly
   setSubmissions(prevSubmissions => 
       prevSubmissions.filter(sub => sub.id !== submission.id)
   );
   ```

3. **Default Status Filter**
   - PillarReview: Default to `'pending'`
   - SubmissionReview: Default to `'all'` (but still filters out approved/rejected)

4. **Status Filter Options**
   - "All Pending" - Shows pending, submitted, under review
   - "Pending Review" - Shows only pending status
   - "Approved (History)" - View past approvals
   - "Rejected (History)" - View past rejections

### Benefits of Auto-Clear
- ⚡ **Instant Feedback**: Mentors see immediate result of their action
- 🎯 **Focus**: No clutter from already-reviewed submissions
- 🔄 **Efficiency**: No need to manually refresh or filter
- 📊 **Real-time Stats**: Pending count updates automatically
- ✅ **Confidence**: Clear visual confirmation that review was processed

## Status Badge Colors
- **Draft** (Gray): `#6b7280`
- **Pending Review** (Yellow): `#fbbf24`
- **Under Review** (Blue): `#3b82f6`
- **Approved** (Green): `#10b981`
- **Rejected** (Red): `#ef4444`

## Best Practices

### For Students
1. ✅ Check the status of your most recent submission before creating a new one
2. ✅ Read mentor feedback carefully if your submission is rejected
3. ✅ Edit and resubmit rejected submissions with requested changes
4. ✅ Keep your submissions organized by using descriptive titles

### For Mentors
1. ✅ Provide clear, constructive feedback when rejecting submissions
2. ✅ Review submissions in a timely manner
3. ✅ Approve submissions that meet the criteria
4. ✅ Use specific comments to help students improve

## Future Enhancements
- Email notifications when submission status changes
- Bulk submission management
- Advanced filtering and search
- Submission analytics and reports
- Version history for edited submissions
