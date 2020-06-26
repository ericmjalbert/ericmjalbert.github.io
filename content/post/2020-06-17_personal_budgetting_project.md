---
title: "Get Bob to Help With Budgeting!"
tags: [
    "python",
    "finance",
    "project",
]
date: "2020-06-26"
images: ["/2020-06-17_northfolk-Ok76F6yW2iA-unsplash.jpg"]
---

Managing personal finance can be difficult.
My wife and I have put some effort into making sure we stay on top of these things.
Over the years we have gone through many iterations of paper documents and Google Sheets to keep track of our budgets.
Lately I've wondered if there is a way to make this a more complete and approachable process.

To this goal, I've created a personal webapp to manage categorizing spendings and tracking personal savings. I call it Budgeting Bob:
* [Here is the github repo for the project](https://github.com/ericmjalbert/budgeting-bob)
* [Here is a public demo for the project](http://budgeting-bob-demo.herokuapp.com): login with `username = demo` and `password = demo`

I'll first talk about my own viewpoint on how personal finance works.
Then I'll give an [overview]({{< relref "#budgeting-bob" >}}) of the work involved in the Budgeting Bob project.
Following that will be my [self-reflections]({{< relref "#project-reflections" >}}) on the project as a whole.

-----

# Personal Finance Management

> Whenever money moves from one place to another I call that a transaction. Personal finance management is just the meaningful analysis of these movements.

Keeping track of one's personal finance is important because otherwise you cannot easily answer basic questions about it.
Simple questions like: 

* "How much money can I spend on food deliveries this month?"
* "Will I be able to go on vacation and still afford rent?"
* "I just got paid, why do I have so little money in my bank account?".

These are the type of questions that personal financing should help with.

The way that I think of it is that every time money moves from one place to another, a "transaction" has just occurred.
To this effect, whenever I get paid, a transaction has just moved money from my employers account into my own savings account.
Whenever I pay off my monthly student debt, I make a transaction from my savings account to my OSAP debt account. Whenever I frivolously spend money on a video game, a transaction has occurred from my VISA account to some external "spendings" account.

That last example outlines the idea of categorizing spendings so that a transaction for rent can be separated from a transaction for entertainment (video games). 
Different categories might have varying importance and it's important to be able to set personal budgets on each category.

Below, I have a simple diagram that outlines this idea. Every line represents transactions that can move money from one node to another:

![Simple Diagram to show how personal wealth moves around](/2020-06-17_transaction_mental_map.png)

To be honest, I'm not an accountant so take this mental idea of finance as just an opinion. Anyways, with that in mind let's get to the actual project.

-----

# Budgeting Bob

![Home page of Budgeting Bob](/2020-06-17_budgeting_bob_home.png)

There were 3 main requirements that Budgeting Bob needed to satisfy:

1. Manage applying categories to transactions.
2. Present a simple view of monthly budgets and their current status.
3. Be able to get an overview of our total wealth overtime.

These breakdown into the three separate feature pages of the application: Transactions, Budgets, and Account Totals.


## Feature 1: Transaction Management

![Transaction pages from demo app](/2020-06-17_budgeting_bob_transactions.png)

* The core problem that this application solves is the managing of transactions.
This means that modeling the transactions is a very important part of it.
After many iterations, the simplest idea was to track how much money a given account has and which transactions are associated to each account.
At the database level this looks like two main tables: `transactions` and `accounts`.
    * For `transactions`, I mostly copied all the data available from RBC's CSV export: `transaction_date`, `account_id`, and `description_1` and `description_2` (RBC provides two distinct values and I keep them separated to assist with category assignments).
    * For `accounts`, I have the needed descriptive information to make them readable: `type` and `owner` (ie. `type="Savings"`, and `owner="Eric"`).
    * I've also included some metadata on the `accounts` table to help with personal bookkeeping: `liquidable`, and `source_of_truth` are to help track where the data for the account comes from and if the account contains usable money. This is needed because some of the accounts are for student debts and car payments.
    * For `accounts`, I also have the `initial_amount`. This is just the amount of money the account had whenever I recorded the first transaction. This value is used in the Account Total page.

I'll also talk about how categories are automatically applied.
Whenever a new transaction is added to the table I check the most recent category for a matching `description_1`.
This gives situations where we'll manually categorize Hydro bill from `description_1='utility bill pmt'`, `description_2='enbridge gas #12023'` and the next time that same `description_1` appears the category will be automatically applied.
The current algorithm has only been tested with RBC's data export, I'm not sure if other banks provide a similar separation of descriptive values.


## Feature 2: Budget Statuses

![Budget report pages from demo app](/2020-06-17_budgeting_bob_budget_report.png)

This page is pretty self-explanatory.
It's just the monthly aggregation of transactions for each category (from the transactions page above).
The monthly budget amounts are set at the database level with the [database initialization script](https://github.com/ericmjalbert/budgeting-bob/blob/master/initialize_db_demo.sh).

For us, this is the main value proposition of using Budgeting Bob. My wife and I needed a way that was dead-simple to check on our status, so that's what this page satisfies.
To further this, I've also added another column "Overall Overage" (which probably has a more official financial term).
The idea of Overall Overage is that I wanted to handle cases where we pay for a cat clinic visit and the cat budget is 10x higher than it should be for that one month.
This is "okay" because we only pay that cat clinic visit once a year, but planning the budget is difficult because it's so skewed.
The Overall overage is just adding all the `Remaining Amount` values from all previous months so we can see if we're approaching zero.
If that value is around 0, then the budget is good, if it's way over than it might indicate that we're consistently over budget and need to adjust.

## Feature 3: Account Total Graphs

![Account totals pages from demo app](/2020-06-17_budgeting_bob_account_totals.png)

The accounts total graph is just a simple way to get all our accounts in one page.
This data comes free since we're already tracking all the transactions and we have the `initial_amount` for each account.
Using this page helps for double checking values since it should agree with each individual bank account.

The daily graph is the leftover from a scrapped feature.
I originally planned to have a way to forecast how much money we'd have for the next `n` months, to help with long-term planning.
To complete this I was using linear regression and having another slider that selected the data range to use for building the line.
Without getting too much into the details, this feature was taking more time than I wanted and it wasn't going to add much value since we could already approximate using the graph.
Also my wife did not care about forecasting so it wasn't really worth it.

About the visualization, I originally used `Chart.js` but really wanted to have a slider for date picking.
While researching how to do this I found [this example](http://www.amcharts.com/demos/line-chart-with-scroll-and-zoom/#theme-light).
I thought that it was the **perfect** solution to a problem I didn't really know how to solve otherwise, so I swap from `Chart.js` to `am4chart`.


## Other Requirements

There were lots of other *minor* requirements that I needed for this to be fully functional. 

#### Working with Heroku
I wanted to have a simple cloud platform to host my application.
I also did not want to spend any money.
Heroku is awesome and I've used it in the past so I decide to use it for a simple setup.

#### Demo mode
I wanted to have a way to show case this project without publicly revealing my personal bank information.
This led to a [demo mode](http://budgeting-bob-demo.herokuapp.com) that had fake data.

Because this was hosted on Heroku it was very easy to setup the separate workflow for demo deployments, since I just created a new heroku app using the same repo and just added a new `heroku-demo` remote to my local git repo.
This way I can do deploys to `git push heroku-demo` and `git push heroku`.
The only hard part about this was to generating the fake demo data, which I managed by altering my real transaction data with some random numbers. The actual script can viewed [here](https://github.com/ericmjalbert/budgeting-bob/blob/master/fill_demo_data.sh).

#### Database Initialization
I originally wanted to use Flask to manage the database, but I ended up doing a custom bash script since I did the original setup manually.
This isn't very clean but it works in this case.
I think next time though I'll actually write out the data models and let `Flask` and `SQLalchemy` manage the database, since it would simplify the full workflow.

#### RBC Transaction Automation
I currently use RBC as my bank of choice.
To get transactions from RBC they have a "Download Transactions" page, which allows users to get a CSV of all the transactions.
Using [Selenium](https://selenium-python.readthedocs.io/), I wrote an experimental script that navigates to that page and automated the data entry from this CSV export.
Ideally I'd use the [RBC Developer API](https://developer.rbc.com/) but I was never able to successfully register.

-----

# Project Reflections

I want to take a step back to write down some of the self-reflections I had on this project.

## What Did I Enjoy

* Working with Heroku was very easy for both local and deployments.
* Working with [jinja2](https://jinja.palletsprojects.com/en/2.11.x/) is interesting because it always has the features that I need, I just never really know what the terms are called.
Using Macros was useful for keeping DRY, but I didn't know what they were called originally so I had to search more than I'd like.
* Working with my wife on planning Budgeting Bob was nice.

## What Did I Dislike

* Login Authentication. I'm not confident enough with writing security systems for web applications. I think it's something I'll need to research a bit more moving forward.
* [RBC Developer API](https://developer.rbc.com/) portal never responded to me when I requested access. Which caused me to use Selenium....
* Using Selenium for the RBC automation. It's a hacky, messy, and unreliable workflow; I think next time I do a brute-force web scraping task I might take a step back and research other solutions first.

## What Did I Find Difficult

* Front end development, feels like I'm actively working against myself when I do anything. Probably because I never actually took a holistic approach to the front-end. I think next time I do some serious front-end work I might try using a front-end library like React.
* Having Heroku handle some of the variables and having others handled by local `.env` files made some things confusing.

## What Did I Learn

* Getting **just** the Minimal Viable Product is extremely useful.
My wife and I have been successfully using Budgeting Bob for many months now, even while it was still in development.
The only things we needed was the database to store transactions and the budget status page.
At first I was manually downloading the CSV and writing SQL queries to `UPDATE` the categories of those transactions.
The workflow was painful but it helped prioritize the next steps (Working on automating these steps).
Overtime little changes were developed and that turned Budgeting Bob into something that is easier and more useful, but the MVP was still functional.
If I waited until all the features were completed before using it I might have had a very different application that wouldn't solve the actual problems we had.
* Not using `SQLalchemy` to manage the data models means you have to write a bunch of stuff yourself. Lesson learned is that for web applications I should not do raw SQL queries (via `db.executes`).
* I started the project with local dev work using the production database and so adding the demo workflow was shoehorned in instead of planned.
I think even for personal projects I might consider having a local, staging, and production environment to help at the ending of a project.


* In all honesty, this application is probably overkill for personal financing. If you want to budget just use a Google sheet like: https://themeasureofaplan.com/budget-tracking-tool/.


## What Would I Do Next For This Project

* I've noticed that the application is not very mobile friendly. It runs slower and some of the texts overlaps painfully. I think I would put some effort to profile the application and find out ways to optimize the speed and UI for mobile.

* Create more automation scripts for other accounts.


-----

Thank you for reading this!
