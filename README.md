# simple-gradescope-api

## Since

I missed my first quiz for CS64 which weighted **4.375%** in total. And quiz 1 is a freaking easy one. Now I have to get 100% in each following quiz and the final and each labs to get a A for sure. Goodbye A+ :/

## So

I decided to write a application that can send me emails about deadlines on Gradescope.

## simple?

The api will copy some code from [apozharski/gradescope-api](https://github.com/apozharski/gradescope-api). I don't need that many functions so this repo is a simplified version.

## How to use?

[**alert_email_template.py(deprecated)**](https://github.com/publicqi/simple-gradescope-api/blob/main/alert_email_template.py)

+ Fill out the config informations

+ Use a cron on a server to run this script periodically

[**alert_email_template2.py**](https://github.com/publicqi/simple-gradescope-api/blob/main/alert_email_template2.py)

+ `python3 alert_email_template2.py &`
+ Use 2 threads: one constantly updates dues and send email per 12 hours, the other send email only when the assignment has 12 hours left.

## How to use in detail

[**alert_email_template2.py**](https://github.com/publicqi/simple-gradescope-api/blob/main/alert_email_template2.py) is a wrapper for this tool and is the script I've been using on my server. I think you can deploy this on the csil server(if SMTP service is installed). Here's a little interpretation of this piece of code:

There're two threadings `t1` and `t2`. Thread 1 runs a function calls `update_dues_per_12_hrs` and thread 2 runs `update_when_some_due_has_12_hrs_left`. They do exactly what the function names suggest. Inside the two functions, they update a global object called `dues`(a dict) and calls `send_email` to notify you.

In `update_dues_per_12_hrs`, the thread will sleep 12 hours and run the update&send process. In `update_when_some_due_has_12_hrs_left`, the thread will sleep until any due has 12 hours left. You can read the detailed code yourself.

As for how to deploy this, I simply runs `python3 alert_email_template2.py & `. The ampersand means "running background" in linux. I know there's better ways to deploy this like [supervisor](http://supervisord.org/), but I'm too lazy to use that. Also I implemented a `send_error_email` function to catch any Exception and send an email. Please let me know if that happened.

## PRs

PRs are welcomed. Hopefully you can understand the functions as they're simple and well-named. The only function I did not use is `get_dues_json()` in [account.py](https://github.com/publicqi/simple-gradescope-api/blob/main/pyscope/account.py). You can make a web app based on the json.

## One unrealistic fantasy

Dr.Matni adds **4.375%** extra credit for this project. Or being a little more realistic, I can re-implement it in MIPS if that gives me some extra credit.