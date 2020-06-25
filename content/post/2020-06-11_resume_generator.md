---
title: "How to Automate Job Applications"
tags: [
    "python",
    "resume",
    "nlp",
    "project",
]
date: "2020-06-11"
images: ["/2020-06-11_andrew-pons-6-RhsUzKO6g-unsplash.jpg"]
---

Creating job applications is a needed effort to progress in a professional career. When I do a large batch of job applications I find that I follow one of two main methodologies:
1. Be non-optimal and use the same resume for all job applications. This is easy, but ineffective,
2. Create a specialized job application for each job description that I apply to. This is hard, but tends to yield better results.

If I'm actively searching for a new position I'll tend to do the latter option, but I've started to wonder if there is a better way to handle this. To this end I planned to automate the creation of specialized job applications.

The final product can be viewed on github at [Resume Generator](https://github.com/ericmjalbert/resume-generator).

I'll first give an overview of my work on the project. Following that will be my [self-reflections]({{< relref "#project-reflections" >}}) on the project as a whole.

-----

There are 4 main components to this project:

1. Create a master resume that contains *all* the information about my professional career.
2. Have a repeatable way to create a rendered resume PDF.
3. Parse a given job description into a list of requirements.
4. Intelligently select a subset of the master resume based on the job descriptions requirements.

## Component 1: Create a Master Resume 

* TL;DR I created a JSON object with all my data. Look at my [master_resume](https://github.com/ericmjalbert/resume-generator/blob/master/master_resume/resume.json) to see the result.

Main idea of component is to stop having the difficult task of manually managing my resume.
With each job application I'm currently having to edit the most recent state of my resume and overtime I'm losing details and wasting time hunting down specific information that I've written in the past.
To this end I will convert my resume into a format that is easily readable by both machine and human: JSON.
This master resume will contain *all* my professional bullet points so that I don't lose them over time and it provides an easy place for me to update achievements.

### Notes About Master Resume Format
I was originally going to use [TinyDB](https://github.com/msiemens/tinydb) to manage a local database of jobs descriptions, work highlights, and skills.
With TinyDB, it stores database tables as separate JSON files on the local disk.
The main issue with using it would be that I only need to manage one resume worth of data.
It'd be difficult to manage multiple JSON (or have 1 complex JSON with all the data in one big table)
This idea might be considered more if this project was suppose to serve multiple "master resumes" or if there was some interface to manage foreign keys across the tables, but that is outside the score of this project.

Instead of TinyDB, the choice of following the [JSON Resume](https://jsonresume.org/) schema was made because it's the "easiest" type of format to be human-maintainable.
I originally followed the schema exactly, however I had some problems with the ways "Skills" were stored and diverged to my own type of JSON resume schema.
The main differences are in the Education and Skills:

```python
@dataclass
class Education:
    """Model Academic experiences and highlights"""

    institution: str
    area: str
    studyType: str
    startDate: str
    endDate: str
    # I removed the "gpa" and courses field from JSON Resume
    #   gpa: str
    #   courses: List[str]
    # I added "thesis" and "publications"
    thesis: str = None
    publications: str = None


@dataclass
class Skills:
    """Model skill highlights"""

    name: str
    # I removed the "level" field from JSON Resume
    #   level: str
    keywords: List[str]
```

This change meant I couldn't use any pre-built tools for [Validating JSON resumes](https://github.com/kelvintaywl/jsonresume-validator).
But turns out that it wasn't really a huge detriment since I could setup an easy `pytest` to do some simple validations. 

```python
from resume_generator.general.resume import Resume

def test_resume_file_is_valid():
    json_resume = Resume()
    assert json_resume.validate()  # Custom method to check types and existence on some keys


def test_resume_file_can_fail():
    fake_resume_data = json.dumps({"fake_resume": "blahblah"})
    fake_resume_file = io.StringIO(fake_resume_data)
    with pytest.raises(TypeError):
        Resume(fake_resume_file)
    fake_resume_file.close()


def test_resume_fields_can_be_accessed():
    test = Resume()
    test.basics.name
    test.basics.location
    [job.company for job in test.work]
    [skill.keywords for skill in test.skills]
```

The other benefit to writing my own validator is that I didn't need to include dummy values for "required" fields of the original schema (eg. `location.address` and some entire sections like `interests` and `volunteer`).

### Notes About Using `dacite`
As part of this project, I wanted to **really** get to know `@dataclass` in python, so I tried modelling everything using it.
I ended up using [`dacite`](https://github.com/konradhalas/dacite) as a "shortcut" to parse a JSON into a `dataclass` because doing something like that seemed like such an obvious pattern to use.
Retrospectively, I think it might have been easier for readability to not use the package because now I have this "magic" function that just handles the initializations.
That being said, it's pretty slick and easy to use, so I think I'll accept the loss of readability for the ease that it brings.


## Component 2: Repeatable Way to Render Resume

* TL;DR I used [best-resume-ever](https://github.com/salomonelli/best-resume-ever) to a moderate amount of success and generated a PDF resume. I still think my original resume looks better though....

![Old and new resume comparison](/2020-06-11_resume_compare.png)

This phase is the bread and butter of this entire project.
It represented the main pain point I had with my job application process and so I needed to have a way to generate a PDFs.

### Which Format To Render: PDF Or `docx`
Because of historic problems with creating a `docx` version of my resume, the initial plan was to have that be the primary format for rendering.
From `docx` it's pretty easy to get a nice PDF; whereas PDF's formatting tends to get mangled when converting to `docx`.
The problem is that no one really has anything that does this out of the box, and using API's and libraries that create `docx` are pretty hard to work with.
After some effort on testing different ways to do this, I decided to focus on an easy setup to creates a PDF version of my resume.
`best-resume-ever` does the one button creating step and it's simple enough for me to understand how to edit the existing templates.

### About the External Project Repo

Using the external tool `best-resume-ever` involves another project repo in my workflow.
This is not really ideal, but with a problem installation automation and environment variables to handle finding the external repo, we're able to work with it in an easy way.
I could probably invest more time into a cleaner solution for this, but since it works and is not a real bottleneck it does not make sense to worry about at this point.

Together with the master resume I am now able to generate a resume; just a very large one that renders every single bullet point in my master resume.

## Component 3: Job Description Parser

* TL;DR Took a simple approach and just grabbed every bullet point (`<li>` tag) that matches some basic conditions. Turns out this includes company benefits. 

Now we are starting to get into the more unique part of the project, this is what separates it from a basic "Create-a-resume" to a "Automatically-customized-resume" project.
Because remember, the whole point of this is to have a subset of my master resume be used to create a specially tailored job application.
To even be able to do that, I needed to be able to scrap the job requirements from an online job description.
Because every single job description has the same idea of using bullet points to list out the requirements, I just need to grab the `<li>` tags using a simple tool to parse HTML: I chose [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/).
This is overall pretty easy besides a few simple edge cases:

* List of links in the footer for site navigation; just remove points with `<a>`.
* Nonsense `<li>` elements in the header; just remove points that are too short (< 4 words)


There is one interesting issue that couldn't be easily solved with the simple approach of grabbing `<li>` tags.
Almost every job description also includes a section dedicated to the company selling themselves to you.
This is very appreciated as a potential candidate, but they are very clearly not suppose to be requirements for a custom job application.
A resume shouldn't specifically put a skill bullet point that says "I am excellent at ping pong" just because the company mentions they regularly have ping pong tournaments.
Here is a striped down example of job application that does this:

![Example job scraping problem](/2020-06-11_example_job_scraping.png)


If I naively pull just the `<li>` points I'll be including all the "compensation" bullet points.
To fix this I attempted futile efforts to read the parents `<div>` to see if it said "Compensation" or "What we offer", but that was overly complex.
Instead I decided to create a list of "company benefit words" that are used in cases that are most often not an actual job requirement:
```python
company_benefit_word_list = [
            "annual",
            "benefits",
            "catered",
            "coffee",
            "company retreat",
            "great place to work",
            "groceries",
            "healthcare",
            "laptop",
            "ping pong",
            "retirement",
            "salary",
            "vacation",
            "we offer",
            "weeks",
        ]
```

This has the problem that I might over ambitiously remove a legitimate job description point, but I think I'm safe with most of these.

### Job Description Output

The parsing of a job description produces a list of strings that represent the job's description.
From the above HTML page, it would produce the following job description list:
```python
[
    "You have experience in SQL: You've used written complex SQL queries that join across data from multiple systems, matching them up even when there was not a straightforward way to join the tables. You've designed tables with an eye towards ease of use and high performance. You've documented schemas and created data dictionaries.",
    "You are a skilled written communicator. We are a 100% remote team and writing is our primary means of communication.",
    "You appreciate our team's values of eagerness to collaborate with teammates from any function of the organization or with any level of data knowledge, iterating over your deliverables, and being curious.",
    "You understand that the perfect is the enemy of the good and default to action by shipping MVP code and iterating as needed to get towards better solutions."
]
```


## Component 4: Create "Intelligent" Subset of Master Resume

* TL;DR Used the most simple implementation. Made it work using [Universal Sentence Encoder](https://tfhub.dev/google/universal-sentence-encoder/4) and [cosine similarities](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.pairwise.cosine_similarity.html) to find the resume highlight that is most relevant to the job description.

This is the "Data Science" part of the project.
To get a specialized resume for a job application I needed a way to take a subset of my master resume.
For this I used [Universal Sentence Encoder](https://tfhub.dev/google/universal-sentence-encoder/4) to convert the text into a vector and then for each highlight of my master resume I would use [cosine similarities](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.pairwise.cosine_similarity.html) to assign a score for each highlight.
This score would be the "closeness" that a resume highlight has with all the job description points.
Summing up these individual values give a score to the resume highlight.
By getting the score for each resume highlight I just need to select the top 2-4 resume highlights per work-experience and now I have a resume that is tailored for the given job description.

Let's run through a simple example to see this in action.

### Simple Example 

Let's assume my master resume has 2 resume highlights:
```python
"work": [
  {
    "company": "Cool Company, Inc.",
    ...
    "highlights": [
        "I used my experience at planning projects and communicating with stakeholders to remove inefficiencies in the day-to-day workflow.",
        "My expertise with AWS helped architecture a scalable infrastructure."
    ]
}
```

These are both legitimate highlights for a developer, but the first highlight is better for a project manager and the second is better for software architects or start-ups.

Let's say we have some obvious job description bullets like:

> * "Experienced with managing large projects."
> * "Skilled at communicating with leadership team."
> * "Handle everyday planning of tasks and duties."

The way the algorithm works is that we convert every text sentence into a vector representation using the [Universal Sentence Encoder](https://tfhub.dev/google/universal-sentence-encoder/4).
Without getting into too much details this essentially turns the sentence, "Experienced with managing large projects", into a list of 512 numbers between -1 and 1.
This list of numbers (vector) represents the "meaning" of the sentence in numbers that can be compared against the other vectors. 

Using the vector encoding of each resume highlight I can calculate the "closeness" of each Job description point.
The "closeness" is calculated using [cosine similirities](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.pairwise.cosine_similarity.html), which is essentially doing computations against the angle between the two vectors.
A cosine score of 1 is the the most similar you can be, a cosine score of -1 is as opposite you can be. 
The final aspect is to take the summation of each cosine score to get a single value for each resume highlight.

Lets go back to our example, pulling in the resume highlights and job descriptions we get the real values of:

```shell
RESUME_HIGHLIGHT: "I used my experience at planning projects and communicating 
  with stakeholders to remove inefficiencies in the day-to-day workflow."
JOB_DESCRIPTIONS:
  "Experienced with managing large projects."      | cosine score: "0.3377"
  "Skilled at communicating with leadership team." | cosine score: "0.1514"
  "Handle everyday planning of tasks and duties."  | cosine score: "0.2358"
OVERALL_SCORE: "0.7249"
     
RESUME_HIGHLIGHT: "Used AWS to architecture a scalable infrastructure."
JOB_DESCRIPTIONS:
  "Experienced with managing large projects."      | cosine score: "0.2326"
  "Skilled at communicating with leadership team." | cosine score: "0.0856"
  "Handle everyday planning of tasks and duties."  | cosine score: "0.1974"
OVERALL_SCORE: "0.5156"
```

In this case, the higher overall score suggests that we should select the highlight that is more "Project Manager" since it scored higher.

### Problems With Scoring Algorithm

This methodology has never actually been tested or compared to others.
I've manually checked that the output is different between job descriptions, but really only tested it on 3 application.
It would make **much** more sense to compare this to other methods and actually have some workflow for testing and improving it.
But at this point I just wanted to start using this project to apply to jobs so I settled for the first thing that worked.

An obvious next step would be to start testing this by scraping LinkedIn or whoishiring.io for a massive amount of jobs and seeing the difference in resume generation over large databases.
This could be accomplished by making a resume that has obvious project management resume highlights and obvious software developer resume highlights and counting how many times the correct resume points make it into the subset.
However, this is all future work.


## What Automatic Resume Generation Looks Like:

Because there are many components that are needed for the full resume to be generated. I've moved all of the steps into a [Makefile](https://github.com/ericmjalbert/resume-generator/blob/master/Makefile) to simplify the workflows. Below is an example of a "job application" using this project (~30 seconds)

![example run of resume generator](https://github.com/ericmjalbert/resume-generator/blob/master/assets/example_application.gif?raw=true)

---

# Project Reflections

I want to take a step back to write down some of the self-reflections I had on this project.

## What Did I Enjoy

Working with `Makefile`. I used to use them a lot back in Grad school and haven't really used it for anything real in a while. But the ability to encapsulate a workflow into a single command is very useful whenever you have multiple technologies interacting with each other. I'm not sure I'll use it for every project, but it was easy enough to work with. 

## What Did I Dislike

When writing the snapshot cases, I noticed that *sometimes* there were failed tests despite being an exact match. Turns out VIM was adding an `EOL` character to the end of the files whenever I opened it to visually inspect the cases. This would cause previously passing test cases to be failing for reasons that were hard to diagnose.

* The actual fix to this was to add `set nofixendofline` to my `.vimrc` file.

* The clue that helped me identify the problem was when I tried to manually compare the files using `diff` and I saw: "`\ No newline at end of file`"

Adding the `tensorhub` pre-trained model made the normal workflow and test cases run much slower, from less than 1 second to about 30 seconds after optimizations.
This wasn't really an issue, but I noticed that the slower test cases really made my motivation drop and it's something I might try to think about more carefully in future projects.


## What Did I Find Difficult

PDF generation.
Just all of it.
Before landing on `best-resume-ever`, I experimented with many other solutions and they were either annoyingly difficult to work with or inconsistent in the output.
This part of the project also highlighted my weakest technical ability, front-end development.
Which is a skill set I might need to start taking more seriously moving forward.

## What Did I Learn

You don't have to make everything perfectly. 
I was starting to lose motivation by the end of the project.
With the amount of things that were not "quite right" (PDF generation, test cases, complex code structure) I did not see the projects completion coming anytime soon.
The main learning was that I can put off a lot of work to future optimizations, I just needed to have something that "worked".
This helped me to: simplify the ML algorithm (no analysis on the accuracy of the highlight scoring), simplify the test cases (only needed the end-to-end test), and not worry about how the PDF was generated.
These were things that I could improve in the future if they needed to be improved.

## What Would I Do Next For This Project

There are a lot of things that I think need to be worked on for this project, but at a high-level I think it'd be important to:

* Update the scoring algorithm for resume highlights. Not only the ML algorithm (ie. maybe universal sentence encoder isn't the best option), but I also might want to change the way I aggregate the scores together.
    * To expand on that second point, the current setup of summing all the scores for each resume highlight is not good since it might favor resume highlights that do well on multiple bullet points instead of *killing it* on a single bullet point (ie. something that is a 90% match to only 1 bullet might not make the cut compared to others that do 20% match to 5 different bullets).
* Add functionality to make a cover letter (using the same formatting as in the `best-resume-ever`). Not many companies look for cover letters, but I think they still add a nice level of polish to a job application.
* Add a way to update my LinkedIn with the same content as the `master_resume.json` so that I only have to manage it in one place


-----

Thank you for reading this!
