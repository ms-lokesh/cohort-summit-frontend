# Episode Progress Sync - Fix Documentation

## Problem
Episode progress was showing 0% even though overall progress showed 14%. This happened because:

1. **Two separate systems** were tracking progress:
   - **Dashboard stats** (`/api/dashboard/stats/`) - Tracks actual pillar submissions
   - **Gamification episodes** (`/api/gamification/dashboard/student_overview/`) - Tracks episode task completion

2. **No automatic sync** between pillar approvals and gamification episode progress
3. **Season was inactive** - gamification requires an active season

## Solution

### 1. Activated Season
```bash
python3 manage.py shell -c "
from apps.gamification.models import Season
season = Season.objects.first()
season.is_active = True
season.save()
"
```

### 2. Created Sync Script
Created `/backend/sync_episode_progress.py` that:
- Checks each user's approved submissions in all pillars (CLT, CFC, IIPC, SCD)
- Maps submissions to corresponding episode tasks
- Updates gamification episode progress accordingly

### 3. Episode Task Mapping

**Episode 1 - Kickoff:**
- CLT: 1 approved CLT submission
- SCD Streak: LeetCode profile with 10+ problems

**Episode 2 - Build:**
- CFC Task 1: Approved Hackathon submission
- IIPC Task 1: Approved LinkedIn Post
- SCD Streak: Maintained

**Episode 3 - Intensity:**
- CFC Task 2: Approved BMC Video submission
- IIPC Task 2: Approved LinkedIn Connection
- SCD Streak: Maintained

**Episode 4 - Finale:**
- CFC Task 3: Approved GenAI Project submission
- SRI: Social activity (not yet implemented)
- SCD Streak: Maintained

## Usage

### Sync all students
```bash
cd backend
python3 sync_episode_progress.py --all
```

### Sync specific user
```bash
cd backend
python3 sync_episode_progress.py --user username
```

## Results

After running the sync:
- User **713524CS154**: Episode 1 at **50%** (CLT completed, SCD pending)
- User **teststudent1**: Multiple episodes progressed with SCD Streak and BMC Video
- Episode progress now reflects actual submission approvals

## Recommendations

### Automatic Sync (Future Enhancement)
Add signal handlers in pillar apps to automatically update episode progress when submissions are approved:

```python
# In apps/clt/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CLTSubmission
from apps.gamification.services import EpisodeService
from apps.gamification.models import Season, Episode

@receiver(post_save, sender=CLTSubmission)
def sync_clt_to_episode(sender, instance, **kwargs):
    if instance.status == 'approved':
        season = Season.objects.filter(is_active=True).first()
        if season:
            episode = Episode.objects.filter(season=season, episode_number=1).first()
            if episode:
                EpisodeService.mark_task_completed(instance.user, episode, 'clt')
```

### Manual Sync When Needed
Run the sync script:
- After bulk approval of submissions
- When migrating to the gamification system
- When debugging progress issues
- Weekly maintenance to catch any missed syncs

## Verification

Check a user's episode progress:
```bash
python3 manage.py shell
>>> from django.contrib.auth import get_user_model
>>> from apps.gamification.models import EpisodeProgress
>>> User = get_user_model()
>>> user = User.objects.get(username='713524CS154')
>>> progress = EpisodeProgress.objects.filter(student=user).first()
>>> progress.clt_completed, progress.scd_streak_active
(True, False)
```

Or via API:
```bash
curl -H "Authorization: Bearer <token>" \
  http://localhost:8000/api/gamification/dashboard/student_overview/
```

## Notes

- Episode 1 must be unlocked (default) for students to see any progress
- Subsequent episodes unlock only after previous episode completion
- SCD Streak requires 10+ problems solved on LeetCode
- Frontend will automatically display updated progress on refresh

---
Last Updated: February 20, 2026
