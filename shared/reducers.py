from datetime import datetime
from shared.types import ProgressDict


def merge_progress(left: ProgressDict, right: ProgressDict) -> ProgressDict:
    """
    Merge two progress dictionaries.
    
    When multiple nodes update progress concurrently, we need to merge their updates.
    This function handles merging of progress states from parallel nodes.
    """
    # Start with a copy of the left (existing) progress
    merged = left.copy()
    
    # Update current_step to the right's value (latest update)
    merged["current_step"] = right.get("current_step", left.get("current_step", ""))
    
    # Merge completed_steps (union of both lists, preserving order)
    left_completed = left.get("completed_steps", [])
    right_completed = right.get("completed_steps", [])
    
    # Add new completed steps from right that aren't in left
    for step in right_completed:
        if step not in left_completed:
            left_completed.append(step)
    
    merged["completed_steps"] = left_completed
    
    # Merge step_times (combine both dictionaries)
    left_times = left.get("step_times", {})
    right_times = right.get("step_times", {})
    
    # Update with new times from right
    for step, times in right_times.items():
        if step not in left_times:
            left_times[step] = times
        else:
            # Merge times for the same step
            if "start" in times:
                left_times[step]["start"] = times["start"]
            if "end" in times:
                left_times[step]["end"] = times["end"]
    
    merged["step_times"] = left_times
    
    # Use the most recent start_time
    if "start_time" in right:
        merged["start_time"] = right["start_time"]
    elif "start_time" not in merged:
        merged["start_time"] = datetime.now()
    
    # Status priority: error > running > completed
    left_status = left.get("status", "running")
    right_status = right.get("status", "running")
    
    if left_status == "error" or right_status == "error":
        merged["status"] = "error"
    elif left_status == "running" or right_status == "running":
        merged["status"] = "running"
    else:
        merged["status"] = "completed"
    
    # Merge error messages (concatenate if both have errors)
    left_error = left.get("error_message")
    right_error = right.get("error_message")
    
    if left_error and right_error:
        merged["error_message"] = f"{left_error}; {right_error}"
    elif right_error:
        merged["error_message"] = right_error
    elif left_error:
        merged["error_message"] = left_error
    
    return merged
