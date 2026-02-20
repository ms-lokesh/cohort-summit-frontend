# Season Score Calculation Fix

## Problem
Season scores were showing 0/1500 even though users had completed tasks and had approved submissions. The scores weren't being calculated incrementally as tasks were completed.

## Root Cause
1. **Scores only calculated at finalization**: The `SeasonScoringService.finalize_season()` method only calculated scores after ALL 4 episodes were completed
2. **No incremental updates**: When tasks were marked as completed via `EpisodeService.mark_task_completed()`, the season score wasn't updated
3. **Date range filters**: Original scoring methods filtered by season start/end dates, which might not have been set correctly

## Solution Implemented

### 1. Created `update_season_score()` Method
Added a new method in `SeasonScoringService` that can be called incrementally:

```python
@staticmethod
@transaction.atomic
def update_season_score(student, season):
    """
    Update season score based on current progress
    Can be called incrementally as tasks are completed
    """
    season_score, created = SeasonScore.objects.get_or_create(
        student=student,
        season=season
    )
    
    # Calculate pillar scores
    season_score.clt_score = SeasonScoringService._calculate_clt_score(student, season)
    season_score.iipc_score = SeasonScoringService._calculate_iipc_score(student, season)
    season_score.scd_score = SeasonScoringService._calculate_scd_score(student, season)
    season_score.cfc_score = SeasonScoringService._calculate_cfc_score(student, season)
    season_score.outcome_score = SeasonScoringService._calculate_outcome_score(student, season)
    
    season_score.calculate_total()
    season_score.save()
    
    return season_score
```

### 2. Updated `mark_task_completed()` to Trigger Score Updates
Modified `EpisodeService.mark_task_completed()` to call `update_season_score()` after marking a task complete:

```python
# Update season score incrementally
SeasonScoringService.update_season_score(student, episode.season)
```

### 3. Fixed Scoring Calculation Methods
Removed date range filters from scoring methods to properly count all approved submissions:

**CLT Scoring (100 points):**
```python
approved_submissions = CLTSubmission.objects.filter(
    user=student,
    status='approved'
).count()

if approved_submissions >= 1:
    return 100
```

**IIPC Scoring (200 points):**
- LinkedIn Post: 100 points
- LinkedIn Connection: 100 points

**CFC Scoring (800 points):**
- Hackathon: 200 points
- BMC Video: 200 points
- GenAI Project: 200 points
- Internship: 200 points

### 4. Updated Sync Script
Modified `sync_episode_progress.py` to calculate season scores after syncing episodes:

```python
# Update season score after all episodes synced
season_score = SeasonScoringService.update_season_score(user, current_season)
print(f"  Season Score: {season_score.total_score}/1500")
```

## Results

After running the sync script:

**713524CS154:**
- Episode 1: 50% (CLT completed)
- Season Score: **100/1500** (CLT: 100)

**teststudent1:**
- Episode 3: In Progress (BMC Video completed)
- Season Score: **200/1500** (CFC: 200)

**teststudent2:**
- No approved submissions yet
- Season Score: **0/1500**

## Score Breakdown

| Pillar | Max Points | Criteria |
|--------|------------|----------|
| CLT | 100 | 1 approved certificate submission |
| IIPC | 200 | LinkedIn Post (100) + Connection (100) |
| SCD | 100 | Daily LeetCode streak calculation |
| CFC | 800 | Hackathon (200) + BMC (200) + GenAI (200) + Internship (200) |
| Outcome | 300 | Internship/Placement >= 10 LPA |
| **TOTAL** | **1500** | Sum of all pillars |

## Usage

### Automatic Updates
Season scores automatically update when:
- Mentor approves a task via `/api/gamification/mentor/approve-task/`
- `EpisodeService.mark_task_completed()` is called

### Manual Sync
Run the sync script to recalculate all scores:
```bash
cd backend
python3 sync_episode_progress.py --all
```

Or for a specific user:
```bash
python3 sync_episode_progress.py --user username
```

## Verification

Check scores via API:
```bash
curl -H "Authorization: Bearer <token>" \
  http://localhost:8000/api/gamification/dashboard/student_overview/
```

Check in Django shell:
```python
from apps.gamification.models import SeasonScore
score = SeasonScore.objects.get(student=user, season=season)
print(f"Total: {score.total_score}/1500")
```

## Frontend Display
The student dashboard will now show:
- **Episode Progress**: 50% (task completion)
- **Season Score**: 100/1500 (7%) (points earned)

These are independent metrics:
- Episode Progress = % of required tasks completed in current episode
- Season Score = Total points accumulated across all pillars

---
Last Updated: February 20, 2026
