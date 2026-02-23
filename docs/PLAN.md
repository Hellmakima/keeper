# Keeper

> 💖🌸✨ *Someone special, just to fix you.* ✨🌸💖

**Keeper** is a personal productivity app designed to help you stay accountable by organizing tasks, goals, and habits into one focused system.

# Features

## Calendar
- **main interface**
- shows task and points, and streaks
- mark tasks done
- can also create new tasks

## task
- **one-time/time-less task lists**
- shopping, tasks, etc
- expand and contract
- defined like this
    - name (required)
    - description
    - from time (single time) (default curr time+01:00)
    - to time (default +01:00)
    - points (1 by default)

## habits
- **manage all repeting tasks/habits/goals**
- create with repetition
- expires if not done within time
- defined like this (TBD)
    - name
    - google calendar task like repetition
    - desc
    - type (Boolean/integer)
    - for integer, also add need a goal amount and unit
    - need to input this during mark as complete
    - what is the goal
  - eg. task 'solve 2 math problems' with goal 'Score above 80%' or 'save $10 every month' with goal 'get THAT hoodie'

## metrics
- **some fancy charts, mertics**
- streaks, charts, mostly for people to build their own plugins
- each plugin can provide mertics and those will be shown here

# SETTINGS (.config/keeper)
- config.json
    - themes
    - calendar
        - week start day
        - [weekday] [color]
    - default views, etc
    - show/hide sidebar, topbar, progress bar, bottom bar
    - allow mutation of task beyond expiry
    - reminders
        - sound
        - notifications
    - how long to show done tasks
- keys.json


# Maybe Stuff
- each plugin can export separate reports
- streaks
- sum like add to calendar integration
- colors for tasks and habits
- android app with widget
- a cool progress bar for current view (day, week, month)
- custom notifications
    - for missed stuff, based on goals
    - custome message
- Connect with others
    - Common tasks
    - Push each other towards completion
- Menstrual cycle tracking
    - note occurance and set next occurance
    - maybe note pain level
- bad habit tracker
    - Count negative habits
    - Identify common triggers (time, activity, mood)
- Mark activities for Dopamine, Serotonin, Oxytocin and/or Endorphin to track levels and suggest more of different things

## Mentor Personas
- Describes the icon, notification messages, in-app avtar
- maybe can make it customizable
- custom personas
- examples
    - Normal – Neutral and professional
    - Coach – Motivational and intense
    - Daughter - The one who looks up to you
    - Mommy – Strict but caring
    - Best Friend (Gay Man) – Sarcastic slay all the wayy
    - Best Friend (White Girl) – Hype hype hype

## Plugins
- plugins for things that don't quite fit the app but a good additions
- IDK how to implement plugins, but we'll see
- Export / Import
    - All the data lives on your device.
    - Import from backup zip files
    - Export to:
        - Backup zip files
        - `.xlsx` (Excel) for visualizing your days and habits
- calendar
  - islamic dates toggle
  - full moon and no moon
- food
    - calories
    - protein
    - fats
- finance
    - spent on (cateogory)
    - monthly limits
- clock
    - alarms, timers or stuff like that
- mood
  - mood wheel picker
  - pick broad cateogory
  - pick specific
  - final
  - text note -> why what how, what now anything
  - can stop whenever
  - doesnt have to be too specific
  - enter when done
  - can enter every 5 minutes
  - some message based on picked mood (e.g., happy -> happiness grows by sharing)
- bad habit tracker
  - Mood vs productivity correlations
  - count your bad habits and maybe we can try to find sum common time or activity that induces is related to this and try to keep user away from it

---

## leftbar

Any installed plugins might add to this list
_Numbers might not work if you have more than 9 plugins_
hjkl to navigate
<C-u> to scroll up
<C-d> to scroll down

```
 KEEPER

 [1] Calendar
 [2] Tasks 
 [3] Habits
 [4] Metrics
```

---

## topbar for calendar

```
 [m] Month      [n] New task               [e] Edit     
 [w] Week       [space] Toggle mark done   [D] Delete
 [d] Day
```

---

## topbar for tasks (Yazi Like 2 Pane view)

```
 [n] New task               [e] Edit     [l] Expand
 [space] Toggle mark done   [D] Delete.  [h] Contract
```

---

## Tasks veiw

I am thinking yazi like 2 pane view

```
* groceries            | > Biryani
> Work                 | > Weekend Party
> Trip packing         | - Garlic
- wash car             | - Potatoes
- water plants         | - ~~detergent~~
- ~~trash~~            |
```

---

## Bottombar

```
15:15 Fri 5 Sept                         (q) quit (/) find (?) keybindings 
```

---

```
 KEYBINDINGS
 
 tasks
 n			new task
 n			new repeating task
 d			delete
 e			edit
 ↵			open

 plugin specific (plugin's name here)
 ...
 
 navigation
 1-9       Select a plugin
 h			←
 j			↓
 k			↑
 l			→
 
 view
 .			toggle completed tasks
 r			toggle repeating tasks
 ,p			sort by points 
 ,t			sort by time 
 ,x			sort by expiry
```

---
```
Delete this Task?


[YES]        [NO]
```
---
