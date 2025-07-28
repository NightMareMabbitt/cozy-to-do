from datetime import datetime, timedelta
import json
import os

DATA_FILE = "goals.json"

def get_date_string(offset=0):
    return (datetime.today() + timedelta(days=offset)).strftime("%Y-%m-%d")

class GoalManager: 
  def __init__(self):
      self.data_file = DATA_FILE
      self.goals = self.load_goals()
      self.today = get_date_string()
  
  def load_goals(self):
      if os.path.exists(self.data_file):
          with open(self.data_file, "r") as f:
              return json.load(f)
      return []
  
  def save_goals(self):
      with open(self.data_file, "w") as f:
          json.dump(self.goals, f, indent=2)
  
  def get_goals_for_date(self, date, completed=False):
    return [g for g in self.goals if g["date"] == date and g["completed"] == completed]

  def add_goal(self, text, imported_from=None):
    goal ={
      "date": self.today,
      "text": text,
      "completed": False
    }
    if imported_from:
      goal["imported_from"] = imported_from
    self.goals.append(goal)
    self.save_goals()

  def mark_goals_complete(self, texts):
    for g in self.goals:
      if g["date"] == self.today and g["text"] in texts:
        g["completed"] = True
    self.save_goals()

  def get_today_goals(self):
        return [g for g in self.goals if g["date"] == self.today and not g["completed"]]


  def get_incomplete_yesterday_goals(self):
    yesterday = get_date_string(-1)
    incomplete = [
      g for g in self.goals
      if g["date"] == yesterday and not g["completed"]
    ]
    imported = []

    for g in incomplete:
      if not any(
        existing["text"] == g["text"] 
        and existing["date"] == self.today
        and existing.get("imported_from") == yesterday
        for existing in self.goals
      ):
        self.add_goal(g["text"], imported_from=yesterday)
        imported.append(g["text"])
    return imported

  def get_last_week_goals(self, include_today=False):
    start = datetime.today() - timedelta(days=7)
    end = datetime.today() if include_today else datetime.today() - timedelta(days=1)

    last_week_dates = {
      (start + timedelta(days=i)).strftime("%Y-%m-%d")
      for i in range((end - start).days + 1)
    }

    return [g for g in self.goals if g["date"] in last_week_dates]

  def get_incomplete_last_week_goals(self):
    today = datetime.today()
    start = today - timedelta(days=7)
    return [
      g for g in self.goals
      if not g["completed"]
      and start.strftime("%Y-%m-%d") <= g["date"] < self.today
      and g.get("imported_from") != self.today
    ]
  
  def import_last_week_goals(self):
    imported = []
    for g in self.get_incomplete_last_week_goals():
        new_goal = {
          "text": g["text"],
          "date": self.today,
          "completed": False,
          "imported_from": g["date"]
        }
        self.goals.append(new_goal)
        imported.append(new_goal)
    self.save_goals()
    return imported      
       