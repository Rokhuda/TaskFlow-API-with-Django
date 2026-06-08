from django.utils import timezone


class PriorityMatrixService:
    """Calculate priority performance values for tasks using an Eisenhower-style matrix."""

    @staticmethod
    def calculate_priority_scores(task):
        """Return a dictionary containing urgency, importance, and the final quadrant."""
        urgency = PriorityMatrixService._calculate_urgency(task)
        importance = PriorityMatrixService._calculate_importance(task)
        quadrant = PriorityMatrixService._determine_quadrant(urgency, importance)

        return {
            'urgency_score': urgency,
            'importance_score': importance,
            'quadrant': quadrant,
        }

    @staticmethod
    def determine_quadrant(task):
        """Compute only the task priority quadrant label."""
        return PriorityMatrixService.calculate_priority_scores(task)['quadrant']

    @staticmethod
    def _calculate_urgency(task):
        """Score urgency based on due date proximity and blocked dependencies."""
        score = 0
        if task.due_date:
            days_until_due = (task.due_date - timezone.now()).days
            if days_until_due < 0:
                # Past due date tasks are highest urgency.
                score += 40
            elif days_until_due <= 3:
                score += 35
            elif days_until_due <= 7:
                score += 25
            elif days_until_due <= 14:
                score += 15
            else:
                score += 5

        # Tasks blocked by other incomplete tasks gain extra urgency.
        if task.blocks.exists():
            blocked_count = task.blocks.count()
            score += min(20, blocked_count * 5)

        return min(100, score)

    @staticmethod
    def _calculate_importance(task):
        """Score importance based on task priority, size, and estimated effort."""
        score = 0
        if task.priority == 'high':
            score += 40
        elif task.priority == 'medium':
            score += 25
        else:
            score += 10

        if task.story_points:
            # Larger tasks are treated as more important for planning.
            score += min(25, task.story_points * 2)

        if task.estimated_hours and task.estimated_hours > 8:
            score += 10

        return min(100, score)

    @staticmethod
    def _determine_quadrant(urgency, importance):
        """Map urgency and importance scores into one of four priority quadrants."""
        if urgency >= 30 and importance >= 30:
            return 'urgent_important'
        if urgency < 30 and importance >= 30:
            return 'not_urgent_important'
        if urgency >= 30 and importance < 30:
            return 'urgent_not_important'
        return 'not_urgent_not_important'
