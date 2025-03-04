# PyTasks
An extremely simple library providing a selection of tasks for users. Each task contains a script that is run after the tasks are commanded to run.

# Usage
The usage is incredibly straightforward and simple.
To create a task, use the function `Task()`

Example:
```
Task("Install MariaDB", """
      echo This is a task to install mariadb
      dnf install mariadb
      echo Finished
    """, selected=False)
```

# Scalability & Portability
This library works on any UNIX-based system with python3 installed (such as Linux, MacOS, and basically all BSDs).

# Primary Use
This program's primary use is to basically act as tasksel but for things beyond just packages.
