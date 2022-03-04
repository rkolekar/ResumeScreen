import io
import warnings

warnings.filterwarnings("ignore")

# import pyresparser
from resume_parser import resumeparse

import docx2txt

from pdfminer3.layout import LAParams
from pdfminer3.pdfpage import PDFPage
from pdfminer3.pdfinterp import PDFResourceManager
from pdfminer3.pdfinterp import PDFPageInterpreter
from pdfminer3.converter import TextConverter

import numpy as np
from nltk import ngrams


def convert_pdf_to_txt(path):
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle, laparams=LAParams())
    page_interpreter = PDFPageInterpreter(resource_manager, converter)

    with open(path, 'rb') as fh:
        for page in PDFPage.get_pages(fh,
                                      caching=True,
                                      check_extractable=True):
            page_interpreter.process_page(page)

        text = fake_file_handle.getvalue()

    # close open handles
    converter.close()
    fake_file_handle.close()
    return text


def convert_doc_to_txt(path):
    MY_TEXT = docx2txt.process(path)
    return MY_TEXT


def call_file_conversion():
    path = "C:\\Users\\BhalchandraK\\PycharmProjects\\ResumeScreen\\ResumeScore\\Resume\\Amit_Mishra.pdf"

    split_filename = path.split('.')
    file_extension = split_filename[1]

    if file_extension == 'pdf':
        return convert_pdf_to_txt(path)
    elif file_extension == 'docx':
        return convert_doc_to_txt(path)
    else:
        return 'Incorrect file format'


def soft_title_match(job_list, cand_list, n=3):
    from test import cand_details_dict

    # from test import cand_details_dict  # imported here to avoid circular dependency error
    soft_title_match.resume_data = resumeparse.read_file(cand_details_dict['pdffile'])

    if (soft_title_match.resume_data["total_exp"]) == 0:  # check years of experience from resume
        return 1
    else:
        final_results = []

        x1 = job_list[0]
        x1 = x1.lower()
        max_count = -1
        max_count_x2 = ""
        max_count_ratio_x1 = 0
        max_count_ratio_x2 = 0

        if len(x1) >= n:
            for x2 in cand_list:
                x2 = x2.lower()
                if len(x2) >= 3:
                    grams_x1 = ngrams(x1.lower(), n)
                    grams_x2 = ngrams(x2.lower(), n)

                    x1_rep = []

                    for grams in grams_x1:
                        x1_rep.append(''.join(grams))

                    x2_rep = []

                    for grams in grams_x2:
                        x2_rep.append(''.join(grams))

                    count = 0

                    for char in x2_rep:
                        if char in x1_rep:
                            count += 1

                    count_ratio_x1 = count / float(len(x1_rep))
                    final_results.append((x1, x2, count_ratio_x1))
                    last_element = final_results[-1]
                    final_score = last_element[-1]
                    return final_results

        else:
            # print("Title is too short")
            # return []
            return []


def get_title_score(x):
    if (soft_title_match.resume_data["total_exp"]) == 0:
        return 1

    else:
        scores = []
        for ele in x:
            scores.append(ele[2])

        scores = np.sort(scores)
        return np.mean(scores[-3:])


def hard_skill_match(job_skills_list, cand_skills_list, resume_path_str):
    if len(job_skills_list) == 0:
        return 0
    try:
        resume_str = convert_pdf_to_txt(resume_path_str)  # this only deals with pdf, not docx files
    except:
        resume_str = ''
    count = 0
    cand_skills_str = " ".join(cand_skills_list)
    for skill in job_skills_list:
        if skill in cand_skills_str:
            count += 1
        elif skill in resume_str:
            count += 1

    # print("Hard skill match score is: "+ str(count / float(len(job_skills_list))))
    return count / float(len(job_skills_list))


def resume_match_score(job_details_dict, cand_details_dict):
    job_details = job_details_dict['title']
    cand_details = cand_details_dict["pdffile"]

    rows = {}
    try:
        data = resumeparse.read_file(cand_details["pdffile"])

        try:
            rows['cand_title'] = data['designition']
        except:
            rows['cand_title'] = []
        try:
            rows['cand_skills'] = data['skills']
        except:
            rows['cand_skills'] = []
    except:
        rows['cand_title'] = []
        rows['cand_skills'] = []

    # Receive Basic Clean skills
    job_title_lis = job_details_dict['title']
    # job_skills_lis = job_details['skills']
    # job_skills_lis = [x.lower() for x in job_skills_lis]

    job_skills_lis1 = job_details_dict["job_skills_lis1"]
    job_skills_lis1 = [x.lower() for x in job_skills_lis1]

    job_skills_lis2 = job_details_dict["job_skills_lis2"]
    job_skills_lis2 = [x.lower() for x in job_skills_lis2]

    job_skills_lis3 = job_details_dict["job_skills_lis3"]
    job_skills_lis3 = [x.lower() for x in job_skills_lis3]

    # total_job_skills = { add all skills here from json }
    total_job_skills = job_details_dict["total_job_skills"]
    total_job_skills = [x.lower() for x in total_job_skills]

    cand_title_lis = cand_details_dict['cand_title']
    cand_skills_lis = cand_details_dict['cand_skills']
    cand_skills_lis = [x.lower() for x in cand_skills_lis]

    # title score
    if len(cand_title_lis) != 0:
        title_score_output = soft_title_match(job_title_lis, cand_title_lis)
    else:
        title_score_output = [('', '', 0)]

    title_score = get_title_score(title_score_output) * 100

    skill_score1 = hard_skill_match(job_skills_lis1, cand_skills_lis, cand_details_dict["pdffile"]) * 100
    skill_score2 = hard_skill_match(job_skills_lis2, cand_skills_lis, cand_details_dict["pdffile"]) * 100
    skill_score3 = hard_skill_match(job_skills_lis3, cand_skills_lis, cand_details_dict["pdffile"]) * 100

    job_skills_rem = []
    for i in total_job_skills:
        if i not in (job_skills_lis1 + job_skills_lis2 + job_skills_lis3):
            job_skills_rem.append(i)

    #   skill_score_remaining
    skill_score_rem = hard_skill_match(job_skills_rem, cand_skills_lis, cand_details) * 100

    x1 = 1
    if len(job_skills_lis1) == 0:
        x1 = 0

    x2 = 1
    if len(job_skills_lis2) == 0:
        x2 = 0

    x3 = 1
    if len(job_skills_lis3) == 0:
        x3 = 0

    x_rem = 1
    if len(job_skills_rem) == 0:
        x_rem = 0

    sum_total = x1 * 0.5 + x2 * 0.2 + x3 * 0.1 + x_rem * 0.2

    x1_wt = 0.5 * x1 / sum_total
    x2_wt = 0.2 * x2 / sum_total
    x3_wt = 0.1 * x3 / sum_total
    x_rem_wt = 0.2 * x_rem / sum_total

    essential_skill = x1_wt * skill_score1
    important_skill = x2_wt * skill_score2
    good_skill = x3_wt * skill_score3

    skill_score = x1_wt * skill_score1 + x2_wt * skill_score2 + x3_wt * skill_score3 + x_rem_wt * skill_score_rem

    # match score - weighted combination of title score, skill score
    match_score = 0.4 * title_score + 0.6 * skill_score

    output = {}
    output['essential_skill'] = essential_skill
    output['important_skill'] = important_skill
    output['good_skill'] = good_skill
    output['skill_score'] = skill_score
    output['title_score'] = title_score
    output['match_score'] = match_score
    return output
    # print("The final output is: ", output)
