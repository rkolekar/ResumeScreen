#import sys

# import test
# import try_resume_screen
from try_resume_screen import resume_match_score

job_details_dict = {
    "title": ["software engineer"],
    "job_skills_lis1": ["Python", "Django", "Flask", "SQL"],
    "job_skills_lis2": ["web-services", "JSON"],
    "job_skills_lis3": ["XML", "Pytorch"],
    "total_job_skills": ["Python", "Django", "Flask", "SQL", "web-services", "github", "Keras", "Pytorch"],
    "requisitionid": 123,
    "job_details_text": "iogngr meg, gewg",
    "skills": {"Organise": 1, "Leadership": 1, "Team Management": 1, "Team Player": 1},
    "minexp": 5,
    "maxexp": 10,
    "minrelexp": 2,
    "maxrelexp": 10,
    "skillandcomp": "ienwfwf efw"
}

cand_details_dict = {
    "cand_skills": ["Python", "Django", "Flask", "Pytorch", "JSON"],
    "cand_details_text": "efiewf ewfwe",
    "candidateid": 1234,
    "pdffile": "C:\\Users\\BhalchandraK\\PycharmProjects\\sample resumes\\Akshay_Milmile.pdf",
    "cand_title": ['software engineer', 'devops', 'software developer', 'channel partners', 'software architect']
}


def run_test():
    final_score = resume_match_score(job_details_dict, cand_details_dict)
    #return resume_match_score(job_details_dict, cand_details_dict)
    # print(final_score)
    return final_score


run_test()
