import tensorflow_hub as hub
from sklearn.metrics.pairwise import cosine_similarity

#####
# Run this whole thing in the root of `resume_generator` repo
#####


def get_cosine_similarity(target, list_of_vectors):
    """Returns only list of similarities for given target vector."""
    all_similarties = cosine_similarity([target[0], *list_of_vectors])
    return list(all_similarties[0])


# This is from the resume-generator/library folder
embed = hub.load("./library/universal-sentence-encoder/")

resume_highlights = [
    "I used my experience at planning projects and communicating with stakeholders to remove inefficiencies in the day-to-day workflow.",
    "Used AWS to architecture a scalable infrastructure.",
]

job_description_bullets = [
    "Experienced with managing large projects.",
    "Skilled at communicating with leadership team.",
    "Handle everyday planning of tasks and duties."
]


def get_score(resume_highlight, job_description_bullets):
    job_embeddings = embed(job_description_bullets)
    similarities = get_cosine_similarity(embed([resume_highlight]), job_embeddings)
    scorings = [value for value in similarities if 0 < value < 1]
    for text, score in zip(job_description_bullets, scorings):
        # the <50 enforces 50 characters and left aligned text
        print(f"  \"{text: <50}\" | score: \"{score:.4}\"")
    total_score = sum(scorings)
    return total_score


for highlight in resume_highlights:
    print("-----")
    print("RESUME HIGHLIGHT:")
    print(f"  \"{highlight}\"")
    print("JOB DESCRIPTIONS AND SCORE")
    score = get_score(highlight, job_description_bullets)
    print(f"OVERALL SCORE: \"{score:.4}\"")
