#!/usr/bin/env python3
"""A CBT App."""
import sys
import sqlite3 as lite


def create_thought_history_log_db(con, cur):
    """Creates the database if it doesn't already exist."""

    con.execute('''CREATE TABLE IF NOT EXISTS THOUGHT_RECORD_HISTORY_LOG (ID INTEGER PRIMARY KEY AUTOINCREMENT,
        LOCATION TEXT NOT NULL,
        EMOTION TEXT NOT NULL,
        NEGATIVE_THOUGHT TEXT NOT NULL,
        EVIDENCE_FOR TEXT NOT NULL,
        EVIDENCE_AGAINST TEXT NOT NULL,
        ALTERNATE_THOUGHT TEXT NOT NULL,
        ALTERNATE_EMOTION TEXT NOT NULL);''')


def create_thought_history_backup_db(con, cur):
    """Creates a backup table to prevent data loss.  Allows user to undo accidental deletes."""

    con.execute('''CREATE TABLE IF NOT EXISTS THOUGHT_RECORD_HISTORY_LOG (ID INTEGER PRIMARY KEY AUTOINCREMENT,
        LOCATION TEXT NOT NULL,
        EMOTION TEXT NOT NULL,
        NEGATIVE_THOUGHT TEXT NOT NULL,
        EVIDENCE_FOR TEXT NOT NULL,
        EVIDENCE_AGAINST TEXT NOT NULL,
        ALTERNATE_THOUGHT TEXT NOT NULL,
        ALTERNATE_EMOTION TEXT NOT NULL);''')


def menu():
    """Main Menu."""

    menu_dict = {
        '1': create_thought_log,
        '2': view_history,
        '3': view_cognitive_distortions,
        '4': delete_entry,
        '5': delete_entire_history,
        '6': quit,
    }

    menu_message_dict = {
        1: "Create a Thought Record",
        2: "View your history",
        3: "View the list of Cognitive Distortions",
        4: "Delete a Thought Record",
        5: "Delete your entire History",
        6: "Quit",
    }

    print("What would you like to do? (Enter a Number)\n\n")

    k = 0
    for k in menu_message_dict:
        s = str(k) + '. '
        print(s, menu_message_dict[k])
        k += 1

    menu_choice = input("\n")

    try:
        menu_dict[menu_choice]()
    except KeyError:
        print("Please pick a valid option")
        menu()


def create_thought_log():
    """Logs the user's thought record & saves to the database."""
    location   = input("Where were you?\n")
    emotion    = input("Emotion or Feeling: \n")
    negative   = input("Negative Automatic Thought: \n")
    evidence   = input("Evidence that supports the thought: \n")
    contradict = input("Evidence that does not support the thought: \n")
    alternate  = input("Alternative thought: \n")
    against    = input("Emotion or Feeling: \n")

    con.execute("INSERT INTO THOUGHT_RECORD_HISTORY_LOG (LOCATION, EMOTION, NEGATIVE_THOUGHT, EVIDENCE_FOR, EVIDENCE_AGAINST, ALTERNATE_THOUGHT, ALTERNATE_EMOTION) VALUES (?, ?, ?, ?, ?, ?, ?)", (location, emotion, negative, evidence, contradict, alternate, against))
    con.commit()
    print("Data logged \n\n")


def view_history():
    """Views user's Thought Record History from database."""
    print("")

    cur.execute("SELECT * FROM THOUGHT_RECORD_HISTORY_LOG")
    for row in cur:
        print("Log Number: ", row[0])
        print("Location:", row[1])
        print("Emotion or Feeling: ", row[2])
        print("Negative Automatic Thought: ", row[3])
        print("Evidence that supports the thought : ", row[4])
        print("Evidence that does not support the thought: ", row[5])
        print("Alternative thought: ", row[6], "\n")
        print("Emotion or Feeling: ", row[7], "\n")


def view_cognitive_distortions():
    """Outputs the list of Cognitive Distortions."""

    # s = 
    distortions_dict = {
        1: "Filtering: magnifying the negative details while filtering out the positive\n",
        2 : 'Black & White Thinking: placing people or situations in "either/or" categories with no shades of grey.  (also known as Zero-Sum Fallacy)\n',
        3 : "Overgeneralization: coming to a general conclusion based on a single incident or piece of evidence.  Seeing things a part of a never-ending pattern of defeat.\n",
        4 : "Jumping to Conclusions: deciding we know how someone's feeling or why they act a certain way without having any input from that person\n",
        5 : "Catastrophizing: expecting disaster to strike, no matter what.  (also called \"magnifying or minimizing\" \n",
        6 : "Personalization: believing that everything others say or do is some kind of direct, personal reaction to ourselves\n",
        7 : "Control Fallacies: feeling externally controlled, and seeing ourself as helpess or a victim of fate.  (also referred to as \"Learned Helplessnes\" \n",
        8 : "Fallacy of Fairness: feeling resentful because we think we know what is fair, both other people won\'t agree with us\n",
        9 : "Blaming: holding other people responsible for your pain, or blaming ourselves for every problem\n",
        10: "Shoulds: having a list of ironclad rules about how we and others should behave.  People who break the rules make us angry, and we feel guilty when we violate them\n",
        11: "Emotional Reasoning: believing that what we feel must be true automatically\n",
        12: "Fallacy of Change: expecting other people will change to suit us if we just pressure or cajole them enough.  Needing to change people because our hopes for happiness seem to depend entirely on them\n",
        13: "Global Labeling: generalizing one or two qualities into a negative global judgement.  Instead of describing an error in context of a specific situation, we attach an unhealthy label to ourselves.\n",
        14: "Always Being Right: continually being on trial to prove that our opinions and actions are correct.  Being wrong is unthinkable, and we will go to any length to demostrate our rightness\n",
        15: "Heaven's Reward Fallace: expecting our sacrifice and self-denial to pay off, as if someone is keeping score.  Feeling bitter when the reward doesn't come"
    }

    for k in distortions_dict:
        s = str(k) + ". "
        print(s, distortions_dict[k])




def delete_entry():
    """Lists entire log history & allows user to delete.  Repositions logs to account for deleted numbers in database."""
    # the repositioning portion of this function is not implemented yet
    print("")

    log_number_to_delete = input('Enter the number of the Log you wish to delete.  If you don\'t know the number, press "v" to View Log, or "m"for Main Menu \n\n')
    log_number_to_delete = int(log_number_to_delete)
    if log_number_to_delete == "v":
        view_history()
    elif log_number_to_delete == "m":
        pass

    else:
        log_number_to_delete = int(log_number_to_delete)
        cur.execute("SELECT * FROM THOUGHT_RECORD_HISTORY_LOG")
        for row in cur:
            cur.execute("DELETE FROM THOUGHT_RECORD_HISTORY_LOG WHERE ID=?;", (log_number_to_delete,))
            con.commit()

    print("Log %d Deleted! \n" % log_number_to_delete)


def delete_entire_history():
    """A Docstring so SublimeLint will Fuck Off."""
    user_delete_decision = input("Are you sure you want to do this??? (Y/N) \n")

    # In the future, add in a password protection here
    if user_delete_decision[0].lower() == "y":
        cur.execute("DELETE FROM THOUGHT_RECORD_HISTORY_LOG WHERE ID IN (SELECT ID FROM THOUGHT_RECORD_HISTORY_LOG)")
        con.commit()

        print("")
        print("Thought Record History Deleted!! \n")

    else:
        print("Nevermind.  Back to the Main Menu")


def quit():
    """Quits the program."""
    print("")
    print("Thanks!  Have an awesome day :) \n")
    sys.exit()


if __name__ == '__main__':
    con = lite.connect('thought_history.sqlite')
    cur = con.cursor()

    create_thought_history_log_db(con, cur)
    create_thought_history_backup_db(con, cur)

    print("\nWelcome to the CBT App :)\n")

    run = True
    while run == True:
        menu()
