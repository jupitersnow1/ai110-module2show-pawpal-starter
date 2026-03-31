import pytest
from pawpal_system import Task


def test_task_methods():
    task = Task(id="t1", description="Feed", duration_min=15, priority="high")
    
    assert not task.is_complete
    task.mark_complete()
    assert task.is_complete
    
    assert task.priority_score() == 3 * 10.0 / 15  # 2.0
    
    task_dict = task.to_dict()
    assert task_dict["id"] == "t1"
    assert task_dict["description"] == "Feed"
    assert task_dict["priority"] == "high"


def test_task_invalid_duration():
    with pytest.raises(ValueError, match="duration_min must be greater than zero"):
        Task(id="t2", description="Walk", duration_min=0, priority="medium")

    with pytest.raises(ValueError, match="duration_min must be greater than zero"):
        Task(id="t3", description="Brush", duration_min=-10, priority="low")

    with pytest.raises(ValueError, match="duration_min must be an integer"):
        Task(id="t1", description="Bath", duration_min='', priority="high")


def test_task_invalid_priority():
    with pytest.raises(ValueError, match="priority must be one of"):
        Task(id="t4", description="Walk", duration_min=15, priority="urgent")

    with pytest.raises(ValueError, match="priority must be one of"):
        Task(id="t5", description="Groom", duration_min=20, priority="unknown")


def test_task_mark_complete_idempotent():
    task = Task(id="t6", description="Check teeth", duration_min=10, priority="low")
    assert not task.is_complete

    task.mark_complete()
    assert task.is_complete

    task.mark_complete()
    assert task.is_complete


def test_task_to_dict_immutability():
    task = Task(id="t7", description="Play", duration_min=20, priority="medium")
    task_dict = task.to_dict()

    # ensure required fields exist
    expected_keys = {"id", "description", "duration_min", "priority", "frequency", "constraints", "is_complete"}
    assert set(task_dict.keys()) == expected_keys
    assert task_dict["id"] == "t7"
    assert task_dict["description"] == "Play"

    # mutate returned dict and verify original object is unchanged
    task_dict["description"] = "Naughty"
    task_dict["is_complete"] = True
    assert task.description == "Play"
    assert not task.is_complete


def test_task_priority_score_ordering():
    # create tasks with different priority/duration combos
    high_short = Task(id="hs", description="High short", duration_min=10, priority="high")  # score: 3*10/10 = 3.0
    high_long = Task(id="hl", description="High long", duration_min=30, priority="high")    # score: 3*10/30 = 1.0
    med_short = Task(id="ms", description="Med short", duration_min=10, priority="medium")  # score: 2*10/10 = 2.0
    low_any = Task(id="la", description="Low any", duration_min=20, priority="low")        # score: 1*10/20 = 0.5

    # assert relative ordering: high/short > med/short > high/long > low
    assert high_short.priority_score() > med_short.priority_score()
    assert med_short.priority_score() > high_long.priority_score()
    assert high_long.priority_score() > low_any.priority_score()

    # test sorting by score descending (higher score first)
    tasks = [low_any, high_long, med_short, high_short]
    sorted_tasks = sorted(tasks, key=lambda t: t.priority_score(), reverse=True)
    assert sorted_tasks[0] == high_short
    assert sorted_tasks[1] == med_short
    assert sorted_tasks[2] == high_long
    assert sorted_tasks[3] == low_any


def test_task_frequency_validation():
    # valid frequencies
    Task(id="fd", description="Feed daily", duration_min=15, priority="high", frequency="daily")
    Task(id="fw", description="Feed weekly", duration_min=15, priority="high", frequency="weekly")
    Task(id="fo", description="Feed once", duration_min=15, priority="high", frequency="once")

    # invalid frequency
    with pytest.raises(ValueError, match="frequency must be one of"):
        Task(id="fi", description="Feed invalid", duration_min=15, priority="high", frequency="monthly")


if __name__ == "__main__":
    pytest.main(["-q"])