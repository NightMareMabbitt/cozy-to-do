import tempfile
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import json
from goal_manager import GoalManager, get_date_string

def create_manager_with_data(goals):
  # Create a temporary file to store the goals
  with tempfile.NamedTemporaryFile(delete=False, mode='w') as tf: 
    json.dump(goals, tf)
    tf_path = tf.name

  #Patch GoalManger to use this file
  manager= GoalManager()
  manager.data_file = tf_path
  manager.goals = goals.copy()
  manager.today = get_date_string(0)

  return manager, tf_path

def test_add_goal():
  manager, tf = create_manager_with_data([])
  manager.add_goal("Test Goal")
  assert any(g["text"] == "Test Goal" for g in manager.goals)
  os.remove(tf)


def test_mark_goal_complete():
  manager, tf = create_manager_with_data([
    {"text": "Finish test", "date": get_date_string(0), "completed": False}
  ])

  manager.mark_goals_complete(["Finish test"])
  assert manager.goals[0]["completed"] is True
  os.remove(tf)

def test_no_duplicate_yesterday_import(): 
  yesterday = get_date_string(-1)
  today = get_date_string(0)
  goals = [
    {"text": "Yesterday Goal", "date": yesterday, "completed": False},
    {"text": "Yesterday Goal", "date": today, "completed": False, "imported_from": yesterday}
  ]

  manager, tf = create_manager_with_data(goals)
  imported = manager.get_incomplete_yesterday_goals()
  #Should not import again
  assert "Yesterday Goal" not in imported
  os.remove(tf)


def test_import_incomplete_yesterday():
  yesterday = get_date_string(-1)
  goals = [
    {"text": "unfinshed goal", "date": yesterday, "completed": False},
  ]

  manager, tf = create_manager_with_data(goals)
  imported = manager.get_incomplete_yesterday_goals()
  assert "unfinshed goal" in imported
  os.remove(tf)

def test_get_last_week_goals():
    today = get_date_string(0)
    days_ago_3 = get_date_string(-3)
    days_ago_8 = get_date_string(-8)

    goals = [
        {"text": "Recent goal", "date": days_ago_3, "completed": False},
        {"text": "Old goal", "date": days_ago_8, "completed": True},
        {"text": "Today goal", "date": today, "completed": True},
    ]

    manager, tf = create_manager_with_data(goals)
    last_week = manager.get_last_week_goals()

    assert any(g["text"] == "Recent goal" for g in last_week)
    assert all(g["text"] != "Old goal" for g in last_week)
    assert all(g["text"] != "Today goal" for g in last_week)

    os.remove(tf)


