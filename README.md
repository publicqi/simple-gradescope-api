# simple-gradescope-api

## Since

I missed my first quiz for CS64 which weighted **4.375%** in total. And quiz 1 is a freaking easy one. Now I have to get 100% in each following quiz and the final and each labs to get a A for sure. Goodbye A+ :/

## So

I decided to write a application that can send me emails about deadlines on Gradescope.

## simple?

The api will copy some code from [apozharski/gradescope-api](https://github.com/apozharski/gradescope-api). I don't need that many functions so this repo is a simplified version.

## How to use?

[**alert_email_template.py** ](https://github.com/publicqi/simple-gradescope-api/blob/main/alert_email_template.py)

+ Fill out the config informations

+ Use a cron on a server to run this script periodically

## PRs

PRs are welcomed. Hopefully you can understand the functions as they're simple and well-named. The only function I did not use is `get_dues_json()` in [account.py](https://github.com/publicqi/simple-gradescope-api/blob/main/pyscope/account.py). You can make a web app based on the json.

## One unrealistic fantasy

Dr.Matni adds **4.375%** extra credit for this project. Or being a little more realistic, I can re-implement it in MIPS if that gives me some extra credit.