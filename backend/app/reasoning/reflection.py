"""Reflection mechanism for agent introspection."""

from typing import Any, Dict, List, Optional
from datetime import datetime


class Reflection:
    """
    Reflection mechanism for agent to analyze its own performance.
    """
    
    def __init__(self):
        """Initialize reflection."""
        self.reflections: List[Dict[str, Any]] = []
    
    def reflect(
        self,
        execution_id: str,
        success: bool,
        observations: List[str],
        lessons: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Reflect on execution.
        
        Args:
            execution_id: Execution ID
            success: Whether execution was successful
            observations: Key observations
            lessons: Learned lessons
            
        Returns:
            Reflection record
        """
        reflection = {
            "execution_id": execution_id,
            "timestamp": datetime.utcnow().isoformat(),
            "success": success,
            "observations": observations,
            "lessons_learned": lessons or [],
            "effectiveness_score": self._calculate_effectiveness(success, observations)
        }
        
        self.reflections.append(reflection)
        return reflection
    
    def get_insights(self) -> Dict[str, Any]:
        """
        Get insights from all reflections.
        
        Returns:
            Aggregated insights
        """
        if not self.reflections:
            return {"message": "No reflections yet"}
        
        total = len(self.reflections)
        successful = sum(1 for r in self.reflections if r["success"])
        avg_score = sum(r["effectiveness_score"] for r in self.reflections) / total
        
        all_lessons = []
        for r in self.reflections:
            all_lessons.extend(r["lessons_learned"])
        
        return {
            "total_reflections": total,
            "success_rate": (successful / total * 100) if total > 0 else 0,
            "average_effectiveness": avg_score,
            "unique_lessons": list(set(all_lessons)),
            "common_observations": self._get_common_observations()
        }
    
    def _calculate_effectiveness(self, success: bool, observations: List[str]) -> float:
        """
        Calculate effectiveness score.
        
        Args:
            success: Execution success
            observations: Observations made
            
        Returns:
            Score 0-1
        """
        score = 0.5 if success else 0.0
        score += len(observations) * 0.05
        return min(score, 1.0)
    
    def _get_common_observations(self) -> List[str]:
        """
        Get most common observations.
        
        Returns:
            List of common observations
        """
        all_obs = []
        for r in self.reflections:
            all_obs.extend(r["observations"])
        
        # Count occurrences
        obs_count = {}
        for obs in all_obs:
            obs_count[obs] = obs_count.get(obs, 0) + 1
        
        # Return top 5
        sorted_obs = sorted(obs_count.items(), key=lambda x: x[1], reverse=True)
        return [obs for obs, _ in sorted_obs[:5]]


# Global reflection instance
_reflection: Optional[Reflection] = None


def get_reflection() -> Reflection:
    """Get or create global reflection."""
    global _reflection
    if _reflection is None:
        _reflection = Reflection()
    return _reflection
