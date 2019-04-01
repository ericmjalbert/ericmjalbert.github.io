Title: Automated Job Application
Date: 2019-03-25 8:23
Modified: 2019-03-25 8:23
Category: Python
Tags: project, resume, automation
Slug: automate-job-application
Authors: Eric Jalbert
Status: published
Summary: A project to automate creating specialized resumes and cover letters based on a given job description.

# Overview

Applying to job is hard.
There are two main methods that one can apply: be unoptimal results by using the same resume for all job applications (easy, but uneffective), or create a specialized job application for each job description you apply to (long, but tends to yield better results).
To this end I intend to automate the creation of specialized job applications.

There are 4 main steps to this:

1. Convert existing resume/cover letter material into a programmatically accessible format ( and a tinydb).
2. Have a repeatable way to create PDF's of resume and cover letter (react-pdf, jinja2 templating)
3. Get a way to parse job descriptions into key bullet points (remove fluff)
4. Automate changing the resume/cover letter context based on job description points (sent2vec?)


## Convert existing material to accessible format

I hate having multiple resumes and coverletters that I have to copy and paste from, getting the formatting all messed up during the process.
To this end I have converted my existing resumes to follow (jsonresume)[https://jsonresume.org/]
