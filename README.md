# Mailgun
Python files that use Mailgun's API

# How to Install
1. [Download and install Python 3.6+](http://python.org/downloads) (make sure to include it in PATH when it prompts you during installation)
2. Open the command prompt (cmd) from the start menu
3. Inside of cmd, type:
```
python
import pip
exit()
pip install requests
pip install prettytable
pip install xlsxwriter
```
4. Download the zip file from GitHub, you should now be able to double click the python files in order to run them.
5. Replace YOUR_API_KEY with your Mailgun API key inside all of the python files.

# Get statistics from message tags (statistics.py)
In this implementation, we have used 4 different tags, the first is LrgEm##, then LrgEm##a, LrgEm##b, and LrgEm##c. This gets the summation of all these tags and bases the results on those numbers. The user only has to enter the first one (LrgEm##). Results are stored in the "results" folder.

![1](https://raw.githubusercontent.com/gopikrishnareddy93/mailgun/master/screenshots/1.png)
![2](https://raw.githubusercontent.com/gopikrishnareddy93/mailgun/master/screenshots/2.png)
![3](https://raw.githubusercontent.com/gopikrishnareddy93/mailgun/master/screenshots/3.png)

# Download email addressess that should be removed (failures.py)
This one gets the email addresses of permanent bounces, unsubscribes, and complaints then puts them into excel files so that you can later upload them for deletion. Results are stored in the "results" folder.

![1](https://raw.githubusercontent.com/gopikrishnareddy93/mailgun/master/screenshots/4.png)

# Download Logs (logs.py)
This gets all of the events that have occured on an email for a specific tag. This also consolidates all the tags for a, b, and c and creates an xlsx spreadsheet. There are also pre-populated fields in the spreadsheet with number of opens, clicks, delivers, fails, open rate, and click through rate. Results are stored in the "results" folder.

![1](https://raw.githubusercontent.com/gopikrishnareddy93/mailgun/master/screenshots/5.png)
![2](https://raw.githubusercontent.com/gopikrishnareddy93/mailgun/master/screenshots/6.png)
