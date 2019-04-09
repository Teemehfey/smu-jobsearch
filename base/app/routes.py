import json, requests, socket, os
from flask import render_template, flash, redirect, url_for, request, jsonify, send_from_directory
from app import app, db
from app.forms import *
from flask_login import current_user, login_user, logout_user,login_required
from app.models import *
from app.sysmon import *
from werkzeug.urls import url_parse
from wtforms.validators import ValidationError
from sqlalchemy import func, or_
from werkzeug import secure_filename
from flask_wtf.file import FileField
from werkzeug.utils import secure_filename
import math


# @app.route('/weisheng',methods=['GET','POST'])
# def weisheng():
#     messages = False
#     if current_user.is_authenticated:
#         return redirect(url_for('index_reg'))
#     form = LoginForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(email=form.email.data).first()
#         if user is None or not user.check_password(form.password.data):
#             # flash('Invalid username or password')
#             messages = True
#             return render_template('login2.html', title='Sign In', form=form, messages=messages)
#         login_user(user)
#         if user.role == 'regular':
#             return redirect(url_for('index_reg'))
#         elif user.role == 'admin':
#             return redirect(url_for('index_admin'))
#
#     return render_template('login2.html', title='Sign In', form=form)
#
# @app.route('/weisheng2', methods=['GET','POST'])
# def weisheng2():
#     not_smu_email = False
#     if current_user.is_authenticated:
#         return redirect(url_for('index_reg'))
#     form = RegistrationForm()
#     if form.validate_on_submit():
#         if 'smu.edu.sg' in form.email.data:
#             user = User(email=form.email.data, role='regular', gender='')
#             user.set_password(form.password.data)
#             db.session.add(user)
#             db.session.commit()
#             return redirect(url_for('weisheng'))
#         else:
#             not_smu_email = True
#             return render_template('register2.html', title='Register', form=form, not_smu_email=not_smu_email)
#     return render_template('register2.html', title='Register', form=form)



@app.route('/')
@app.route('/index_reg')
@login_required
def index_reg():
    try:
        #########1st part, sorting and gettign 3 top jobs based on impressions 
        job_application = JobPost.query.all()
        max_list = []
        max_length = 0
        for job in job_application:
            impressions = job.impressions
            print(impressions)
            new_list = impressions.split(',')[0:-1]
            count = len(new_list)
            if count >= max_length and len(max_list) < 3:
                max_list.append(job)
                continue;

            if count >= max_length and len(max_list) == 3:
                max_list.pop()
                max_list.append(job)

        ##########2nd part of api, sorting the 3 jobs by application)
        job_applications = Application.query.all()
        locmap = {}
        for job in job_applications:
            attrs = job.jobpost_id
            if(attrs not in locmap):
                locmap[attrs] = 1
            else:
                locmap[attrs] += 1

        #this is a sorted list of job id and applications in the ascending form of [[jobid, no_of_apps], [jobid2, no_of_apps2]]
        sorted_d = sorted(locmap.items(), key=lambda x: x[1])
        #top 3 job IDs by application count below
        top3_list = sorted_d[(len(sorted_d)-3):(len(sorted_d))]
        top3_ids = []
        #get the list of top 3 job_post_ids
        for item in top3_list:
            top3_ids.append(item[0])

        #define the list that will contain the top 3 job_post objects
        top3_by_applications = []

        for item in top3_ids:
            object = JobPost.query.filter_by(id=item).first()
            top3_by_applications.append(object)


        merged_list = max_list + top3_by_applications

        #WAYNE, THIS MERGED_SET IS WHAT YOU WANT FOR THE FEATURED jobs
        #IT CONTAINS THE TOP 5-6 JOBS WE NEED FOR FEATURED LIST
        merged_set = set(merged_list)



        return render_template('index_reg.html',merged_set=merged_set)
        #return jsonify([s.serialize() for s in top3_by_applications])

    except Exception as e:
        return (str(e))


#GET 3 JOBS WITH HIGHEST IMPRESSION
#GET 3 JOBS WITH HIGHEST SIGN UPS

def takeSecond(elem):
    return elem[1]


# @app.route('/api/top3impression/')
# def top3impression():
#     try:
#         job_application = JobPost.query.all()
#         max_list = []
#         max_length = 0
#         for job in job_application:
#             impressions = job.impressions
#             print(impressions)
#             new_list = impressions.split(',')[0:-1]
#             count = len(new_list)
#             if count >= max_length and len(max_list) < 3:
#                 max_list.append(job)
#                 continue;
#
#             if count >= max_length and len(max_list) == 3:
#                 max_list.pop()
#                 max_list.append(job)
#
#         ##########2nd part of api, sorting the 3 jobs by application)
#         job_applications = Application.query.all()
#         locmap = {}
#         for job in job_applications:
#             attrs = job.jobpost_id
#             if(attrs not in locmap):
#                 locmap[attrs] = 1
#             else:
#                 locmap[attrs] += 1
#
#         #this is a sorted list of job id and applications in the ascending form of [[jobid, no_of_apps], [jobid2, no_of_apps2]]
#         sorted_d = sorted(locmap.items(), key=lambda x: x[1])
#         #top 3 job IDs by application count below
#         top3_list = sorted_d[(len(sorted_d)-3):(len(sorted_d))]
#         top3_ids = []
#         #get the list of top 3 job_post_ids
#         for item in top3_list:
#             top3_ids.append(item[0])
#
#         #define the list that will contain the top 3 job_post objects
#         top3_by_applications = []
#
#         for item in top3_ids:
#             object = JobPost.query.filter_by(id=item).first()
#             top3_by_applications.append(object)
#
#
#         merged_list = max_list + top3_by_applications
#
#         #WAYNE, THIS MERGED_SET IS WHAT YOU WANT FOR THE FEATURED jobs
#         #IT CONTAINS THE TOP 5-6 JOBS WE NEED FOR FEATURED LIST
#         merged_set = set(merged_list)
#
#
#
#         return jsonify([s.serialize() for s in merged_set])
#         #return jsonify([s.serialize() for s in top3_by_applications])
#
#     except Exception as e:
#         return (str(e))"""
#
#
#
#
#
# #@app.route('/api/top3application/')
# #def top3application():
#     try:
#         job_applications = Application.query.all()
#         locmap = {}
#         for job in job_applications:
#             attrs = job.jobpost_id
#             if(attrs not in locmap):
#                 locmap[attrs] = 1
#             else:
#                 locmap[attrs] += 1
#
#         #this is a sorted list of job id and applications in the ascending form of [[jobid, no_of_apps], [jobid2, no_of_apps2]]
#         sorted_d = sorted(locmap.items(), key=lambda x: x[1])
#         #top 3 job IDs by application count below
#         top3_list = sorted_d[(len(sorted_d)-3):(len(sorted_d))]
#         top3_ids = []
#         #get the list of top 3 job_post_ids
#         for item in top3_list:
#             top3_ids.append(item[0])
#
#         #define the list that will contain the top 3 job_post objects
#         top3_by_applications = []
#
#         for item in top3_ids:
#             object = JobPost.query.filter_by(id=item).first()
#             top3_by_applications.append(object)
#
#
#
#         #return jsonify([s.serialize() for s in top3_by_applications])
#
#     except Exception as e:
#         return (str(e))
#
#         merged_list = max_list + top3_by_applications
#
#         return jsonify([s.serialize() for s in merged_list])





@app.route('/findjobs',methods=['GET','POST'])
@login_required
def findjobs():
    form = ListingQueryForm()
    querystatus = None
    queried_jobs = None
    count = 0
    kw = []

    if form.validate_on_submit() and form.submit.data:

        if form.keyword.data != '' or len(form.keyword.data) > 1:
            kw = form.keyword.data.split(',')
            keywords_entered = []
            for k in kw:
                keywords_entered.append(k.lower().strip())
            all_jobs = JobPost.query.all()
            keyword_repo = {}
            for job in all_jobs:
                keyword_repo[job.id] = job.keywords.split(',')
            shortlisted_job_ids = {}  #key is id, value is relevance score
            for k,v in keyword_repo.items():
                for value in v:
                    for entered in keywords_entered:
                        if value == entered:
                            if k not in shortlisted_job_ids.keys():
                                shortlisted_job_ids[k] = 1
                            else:
                                shortlisted_job_ids[k] += 1
            queried_jobs_temp = []
            for id,score in shortlisted_job_ids.items():
                jobpost = JobPost.query.filter_by(id=id).first()
                queried_jobs_temp.append([jobpost,score])

            queried_jobs_temp = sorted(queried_jobs_temp,key=takeSecond,reverse=True)

            queried_jobs = []
            for job in queried_jobs_temp:
                queried_jobs.append(job[0])

            if len(queried_jobs) == 0:
                querystatus = 'noresult'
            else:
                count = len(queried_jobs)
                querystatus = 'success'

        else:
            querystatus = 'length'

    else:
        kw = []
        queried_jobs = JobPost.query.all()
        queried_jobs = queried_jobs[0:5]
        count = 5
        querystatus = 'no query'

    return render_template('findjobs.html',queried_jobs=queried_jobs[:5],form=form,querystatus=querystatus, count=count, kw=kw)


@app.route('/findjobs/ajax',methods=['POST'])
@login_required
def findjobsAJAX():
    jsonData = request.get_json()
    kw = jsonData['keywords']
    listing_count = jsonData['listingCount']

    if kw == []:
        data = []
        following_jobs = JobPost.query.all()
        following_jobs = following_jobs[listing_count:listing_count+5]
        for job in following_jobs:
            data.append([job.id,job.title,job.organization,job.timestamp.strftime('%Y-%m-%d'),job.email])
        return jsonify(success=True, data=data)

    else:
        data = []

        all_jobs = JobPost.query.all()
        keyword_repo = {}
        for job in all_jobs:
            keyword_repo[job.id] = job.keywords.split(',')
        shortlisted_job_ids = {}  #key is id, value is relevance score
        for k,v in keyword_repo.items():
            for value in v:
                for entered in kw:
                    if value == entered:
                        if k not in shortlisted_job_ids.keys():
                            shortlisted_job_ids[k] = 1
                        else:
                            shortlisted_job_ids[k] += 1
        following_jobs_temp = []
        for id,score in shortlisted_job_ids.items():
            jobpost = JobPost.query.filter_by(id=id).first()
            following_jobs_temp.append([jobpost,score])
        following_jobs_temp = following_jobs_temp[listing_count:listing_count+5]


        following_jobs_temp = sorted(following_jobs_temp,key=takeSecond,reverse=True)
        for job in following_jobs_temp:
            data.append([job[0].id,job[0].title,job[0].organization,job[0].timestamp.strftime('%Y-%m-%d'),job[0].email])

        return jsonify(success=True,data=data)



@app.route('/applyjob/<id>',methods=['GET','POST'])
@login_required
def applyjob(id):
    form = ApplyJobBtn()
    job = JobPost.query.filter_by(id=id).first_or_404()
    check_appl = Application.query.filter_by(jobpost_id=job.id, user_id=current_user.id).first()
    impressions = job.impressions.split(',')

    if str(current_user.id) not in impressions:
        job.impressions += str(current_user.id) + ','
        db.session.commit()

    applied = False
    if check_appl is not None:
        applied = True

    if form.validate_on_submit():
        if check_appl is None:
            new_application = Application(jobpost_id=job.id, user_id=current_user.id, status='unread',reject_reason='')
            db.session.add(new_application)
            db.session.commit()
            return redirect(url_for('myjobs'))

    return render_template('applyjob.html', job=job,form=form,applied=applied)


@app.route('/myjobs',methods=['GET','POST'])
@login_required
def myjobs():
    applications = Application.query.filter_by(user_id=current_user.id).order_by(Application.timestamp.desc())
    myjoblist = []
    for a in applications:
        myjoblist.append([a,JobPost.query.filter_by(id=a.jobpost_id).first()])
    return render_template('myjobs.html', applications=applications, myjoblist=myjoblist)


@app.route('/myprofile/<id>',methods=['GET','POST'])
@login_required
def myprofile(id):
    user = User.query.filter_by(id=current_user.id).first_or_404()
    form = EditProfileForm()
    comment = []
    if user.resume_loc != '' or user.resume_loc is not None:
        filename = user.resume_loc.split('/')[-1]

    if form.validate_on_submit() and form.submit.data:
        # print(form.resume.data)
        temp = form.keywords.data.split(',')

        if len(temp) <= 10:
            keywords = []

            for keyword in temp:
                keywords.append(keyword.lower().strip())

            keywords = ','.join(keywords)
            print(keywords)

            user.keywords = keywords
            user.gender = form.gender.data
            user.bio = form.bio.data
            user.phone_no = form.phone_no.data

            if form.resume.data is not None:

                if user.resume_loc != '' or user.resume_loc is not None:
                    existing = user.resume_loc
                    if os.path.exists(existing):
                        print('found existing resume, deleting existing')
                        os.remove(existing)

                resume = form.resume.data
                resume.save('/opt/base/base/app/userfiles/resumes/'+resume.filename)
                user.resume_loc = '/opt/base/base/app/userfiles/resumes/'+resume.filename

            db.session.commit()
            comment.append('Changes saved successfully.')
            filename = user.resume_loc.split('/')[-1]
            return render_template('myprofile.html',user=user,form=form,comment=comment,filename=filename)
        else:
            comment.append('Number of Keywords Exceeded')
            form.keywords.data = user.keywords
            return render_template('myprofile.html',user=user,form=form,comment=comment,filename=filename)

    elif request.method == 'GET':
        form.gender.data = user.gender
        form.bio.data = user.bio
        form.phone_no.data = user.phone_no
        form.keywords.data = user.keywords

    return render_template('myprofile.html',user=user,form=form,comment=comment,filename=filename)



@app.route('/myfeedback',methods=['GET','POST'])
@login_required
def myfeedback():
    feedbacks = Feedback.query.filter_by(received=current_user.email)

    return render_template('myfeedback.html',feedbacks=feedbacks)



@app.route('/index_admin',methods=['GET','POST'])
@login_required
def index_admin():

    if current_user.role != 'admin':
        return 'You are not authorized to access this page.'
    else:

        listingscount = 0
        listingid_list = []
        applicantcount_list = []
        unreadcount = 0
        jobtitle_list = []
        impressions_list = []


        listings = JobPost.query.filter_by(email=current_user.email).order_by(JobPost.timestamp)
        for l in listings:
            listingid_list.append(l.id)
            jobtitle_list.append(l.title)
            listingscount += 1
            if l.impressions != '':
                impressions_list.append(len(l.impressions.split(',')) - 1)
            else:
                impressions_list.append(0)


        for id in listingid_list:
            count = 0
            unreadtemp = 0
            applications_for_listing = Application.query.filter_by(jobpost_id=id)
            for a in applications_for_listing:
                count+=1
                if a.status == 'unread':
                    unreadtemp += 1
            applicantcount_list.append(count)
            unreadcount += unreadtemp

        return render_template('index_admin.html', listingscount=listingscount, listingid_list=listingid_list, applicantcount_list=applicantcount_list,
        unreadcount = unreadcount, jobtitle_list=jobtitle_list, impressions_list=impressions_list)



@app.route('/login', methods=['GET', 'POST'])
def login():
    messages = False
    if current_user.is_authenticated:
        return redirect(url_for('index_reg'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            messages = True
            return render_template('login.html', title='Sign In', form=form, messages=messages)
        login_user(user)
        if user.role == 'regular':
            return redirect(url_for('index_reg'))
        elif user.role == 'admin':
            return redirect(url_for('index_admin'))

    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index_reg'))



@app.route('/register', methods=['GET', 'POST'])
def register():
    not_smu_email = False
    if current_user.is_authenticated:
        return redirect(url_for('index_reg'))
    form = RegistrationForm()
    if form.validate_on_submit():
        if 'smu.edu.sg' in form.email.data:
            user = User(email=form.email.data, role='regular', gender='Undefined',keywords='',resume_loc='')
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))
        else:
            not_smu_email = True
            return render_template('register.html', title='Register', form=form, not_smu_email=not_smu_email)
    return render_template('register.html', title='Register', form=form)


@app.route('/mylistings',methods=['GET','POST'])
@login_required
def mylistings():
    form = JobPostForm()
    all_jobs = []
    errors = []

    if current_user.role != 'admin':
        return 'You are not authorized to access this page.'
    else:
        temp_jobs = JobPost.query.filter_by(email=current_user.email).order_by(JobPost.timestamp.desc())
        for job in temp_jobs:
            applications = Application.query.filter_by(jobpost_id=job.id)
            total_count = 0
            unread_count = 0
            pending_count = 0
            for application in applications:
                total_count += 1
                if application.status == 'unread':
                    unread_count += 1
                elif application.status == 'pending':
                    pending_count += 1

            count_list = [total_count,unread_count,pending_count]

            all_jobs.append([job,count_list])

        if form.validate_on_submit():
            temp = form.keywords.data
            temp = temp.split(',')
            keywords = []
            for t in temp:
                keywords.append(t.strip().lower())


            if len(keywords) <= 10:
                keywords = str(','.join(keywords))
                jobpost = JobPost(email = current_user.email, title = form.title.data, organization = form.organization.data, description = form.description.data, pay = form.pay.data, pay_frequency = form.pay_frequency.data, keywords=keywords, impressions = '')
                db.session.add(jobpost)
                db.session.commit()
                return redirect(url_for('mylistings'))
            else:
                errors.append('Keyword Length Exceeded')
                return render_template('mylistings.html', form=form, all_jobs=all_jobs,errors=errors)
        else:
            return render_template('mylistings.html', form=form, all_jobs=all_jobs,errors=errors)


@app.route('/editlisting/<id>',methods=['GET','POST'])
@login_required
def editlisting(id):
    form = EditListingForm(prefix="form")
    form2 = DeleteListingBtn(prefix="form2")
    post = JobPost.query.filter_by(id=id).first_or_404()
    changed = False
    errors = []
    if form.validate_on_submit() and form.submit.data:

        old_keywords = post.keywords
        temp = form.keywords.data
        temp = temp.split(',')
        keywords = []
        for t in temp:
            keywords.append(t.strip().lower())


        if len(keywords) <= 10:
            keywords = str(','.join(keywords))
            post.title = form.title.data
            post.organization = form.organization.data
            post.description = form.description.data
            post.pay = form.pay.data
            post.pay_frequency = form.pay_frequency.data
            post.keywords = keywords
            db.session.commit()
            changed = True
            return render_template('editlisting.html', post=post, form=form, form2=form2, changed=changed, errors=errors)

        else:
            errors.append('Keyword Count Exceeded')
            form.keywords.data = old_keywords
            return render_template('editlisting.html', post=post, form=form, form2=form2, changed=changed, errors=errors)

    elif form2.validate_on_submit() and form2.submit.data:
        application_delete = Application.query.filter_by(jobpost_id=post.id)
        # print(application_delete)
        for a in application_delete:
            db.session.delete(a)
        db.session.commit()
        db.session.delete(post)
        db.session.commit()
        return redirect(url_for('mylistings'))
    elif request.method =='GET':
        form.title.data = post.title
        form.organization.data = post.organization
        form.description.data = post.description
        form.pay.data = post.pay
        form.pay_frequency.data = post.pay_frequency
        print(post.keywords)
        form.keywords.data = post.keywords
    return render_template('editlisting.html', post=post, form=form, form2=form2, changed=changed, errors=errors)

@app.route('/viewapplicants/<id>',methods=['GET','POST'])
@login_required
def viewapplicants(id):
    post = JobPost.query.filter_by(id=id).first_or_404()
    applicants = Application.query.filter_by(jobpost_id=post.id).order_by(Application.timestamp.desc())
    viewapplicants_list = []
    for a in applicants:
        viewapplicants_list.append([a,User.query.filter_by(id=a.user_id).first()])
    return render_template('viewapplicants.html', post=post, applicants=applicants, viewapplicants_list=viewapplicants_list)


@app.route('/viewapplicants/<id>/<user_id>',methods=['GET','POST'])
@login_required
def applicantinfo(id,user_id):
    form1 = AcceptApplicationBtn(prefix="form1")
    form2 = RejectApplicationBtn(prefix="form2")

    post = JobPost.query.filter_by(id=id).first_or_404()
    application = Application.query.filter_by(jobpost_id=post.id,user_id=user_id).first_or_404()
    user = User.query.filter_by(id=user_id).first_or_404()

    resume_name = user.resume_loc.split('/')[-1]

    if application.status == 'unread':
        application.status = 'pending'
        db.session.commit()
    if form1.validate_on_submit() and form1.submit.data:
        application.status = 'accepted'
        db.session.commit()
        return redirect(url_for('viewapplicants',id=post.id))

    elif form2.validate_on_submit() and form2.submit.data:
        application.status = 'rejected'
        application.reject_reason = form2.reject_choice.data
        db.session.commit()

        return redirect(url_for('viewapplicants',id=post.id))
    return render_template('applicantinfo.html', post=post, application=application, user=user, form1=form1, form2=form2, resume_name=resume_name)


@app.route('/givefeedback/<id>/<user_id>',methods=['GET','POST'])
@login_required
def givefeedback(id,user_id):
    form = FeedbackForm()
    receiver = User.query.filter_by(id=user_id).first_or_404()
    application = Application.query.filter_by(jobpost_id=id,user_id=user_id).first()
    if form.validate_on_submit():
        feedback = Feedback(sent=current_user.email,received=receiver.email,feedback_msg=form.feedback.data)
        db.session.add(feedback)
        application.feedback_given = 'Yes'
        db.session.commit()
        return redirect(url_for('viewapplicants',id=id))

    return render_template('givefeedback.html',form=form)


@app.route('/morejobs',methods=['GET','POST'])
@login_required
def morejobs():
    user = User.query.filter_by(id=current_user.id).first_or_404()
    keywords = user.keywords
    url = 'https://www.indeed.com.sg/jobs?q={}&l=Singapore&jt=temporary'.format(keywords)
    return redirect(url)


@app.route('/download_resume/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    uploads = os.path.join(app.root_path, 'userfiles/resumes')
    # print(uploads)
    return send_from_directory(directory=uploads, filename=filename)


######################################################API ROUTES BELOW THIS LINE. 7 IN total########################################################

#ROUTE 1.1 (WORKING). INPUT = USER ID, OUTPUT = NUMBER OF APPLICATIONS AND INFO FOR EACH APPLICATION
@app.route('/api/data/active_applications/', methods=['GET'])
def list_of_active_applications_by_id_or_email():
    if 'id' in request.args:
        try:
            user_id = request.args.get('id')
            job_applications = Application.query.filter_by(user_id=user_id).all()

            if job_applications is None:
                return "This user has no past job applications"

            application_count = 0
            for application in job_applications:
                application_count += 1
            return jsonify([{"application_count:":application_count}, [application.serialize() for application in job_applications]])

        except Exception as e:
            return (str(e))

#ROUTE 1.2 (WORKING) INPUT = DATE, OUTPUT = NUMBER OF APPLICATIONS MADE AND INFO FOR EACH APPLICATION
@app.route('/api/data/application_volume_by_date/', methods=['GET'])
def application_volume_by_date():

    if 'date' in request.args:
        try:
            request_date = request.args.get('date')
            dated_applications = Application.query.filter_by(timestamp=request_date).all()

            if len(dated_applications) == 0:
                return "No applications have been made on this date"
            applicant_count = 0
            for applicant in dated_applications:
                applicant_count += 1
            return jsonify([{"application_count:":applicant_count}, [application.serialize() for application in dated_applications]])
        except Exception as e:
            return (str(e))

#ROUTE 1.3 (INCOMPLETE) WEEKLY APPLICATIONS TO QUERIED JOB LISTING ID. E.g. Enter ID for question asker job, will return total number of applicantcants
#average weekly applicants, no of weeks and the exact number of applicants for each week.

@app.route('/api/data/application_weekly_statistics/', methods=['GET'])
def applications_date_statistics():

    if 'job_id' in request.args:
        try:
            job_id = request.args.get('job_id')
            job_applications = Application.query.filter_by(jobpost_id=job_id).all()

#get total application count

            applicant_count = 0
            for applicant in job_applications:
                applicant_count += 1

            if applicant_count == 0:
                return "No job applications for this job"

#get current date
            curr_datetime = datetime.utcnow()


#get time of earliest application for this job
            date_sorted_list = sorted(job_applications, key=lambda application: application.timestamp)
            earliest_application = date_sorted_list[0]

            #GET TOTAL NUMBER OF DAYS BETWEEN TODAY AND EARLIEST APPLICATION

            time_difference = str(curr_datetime - earliest_application.timestamp)
            split_string = time_difference.split(',')
            days = split_string[0]
            split_days = days.split()

            #THIS VARIABLE BELOW IS THE TOTAL NUMBER OF DAYS
            num_of_dates = split_days[0]

            #GET NUMBER OF WEEKS
            total_weeks = math.ceil((int(num_of_dates))/7)

            #GET AVERAGE APPLICATIONS PER WEEK
            average_per_week = math.ceil(total_weeks/applicant_count)

            #GET A LIST OF SIGN UPS FOR EACH WEEK
            #for week in range(total_weeks):

            return jsonify([{"applicantcount:":applicant_count},{"current_date:":curr_datetime}, {"time_diff:":time_difference},{"total_weeks:":total_weeks}, [a.serialize() for a in date_sorted_list]])

        except Exception as e:
            return (str(e))



#calculate number of weeks that has passed and average weekly applications
#display exact number of applicants for each weeks

#ROUTE 2.1 (WORKING) INPUT = JOB ID, OUTPUT = ALL INFO PERTAINING TO THAT JOB


@app.route('/api/data/job_info/', methods=['GET'])
def job_info_by_id():
    if 'job_id' in request.args:
        try:
            job_id = request.args.get('job_id')
            job_info = Jobpost.query.filter_by(id=job_id).first()
            if job_info is None:
                return "No existing job posts found with matching job ID"
            return jsonify(job_info.serialize())
        except Exception as e:
            return (str(e))

#ROUTE 2.2 (should be working but keeps giving indent fucking error in putty) JOB IDs  BY Keyword
@app.route('/api/data/job_ids_by_keyword/', methods=['GET'])
def job_info_by_keyword():

    if 'keyword' in request.args:
        try:
            keyword = request.args.get('keyword')
            #may need help here to filter with multiple keywords
            jobs = JobPost.query.filter_by(keywords=keyword).all()
            if jobs is None:
                return "No jobs containing such keyword found"

            job_count = 0
            job_array = []
            for job in jobs:
                job_count += 1
                job_array.append(job.id)
                    #will this jsonify even work?

            return jsonify([{"job_listings_count:":job_count}, {"job_listing_IDs:":job_array}])

        except Exception as e:
            return (str(e))



#ROUTE 2.3 RETURN ALL JOB LISTING IDS BY employer ID
@app.route('/api/data/job_ids_by_employer_id/', methods=['GET'])
def job_info_by_emp_id_keyword():

    if 'employer_id' in request.args:
        try:
            keyword = request.args.get('employer_id')

            employer = User.query.get(keyword)
            if employer is None:
                return "No employer with such ID"

            employer_email = employer.email #or employer[0] which one is correct. apparently the current one is

            job_listings = JobPost.query.filter_by(email=employer_email).all()
            if job_listings is None:
                return "No job listings posted by this employer"

            job_count = 0
            job_array = []
            for job in job_listings:
                job_count += 1
                job_array.append(job.id) #### or job[0]???????) NEED HELP HERE
                #now serialize this shit and return it
            return jsonify([{"job_listings_num:":job_count}, {"job_listing_IDs:":job_array}])

        except Exception as e:
            return (str(e))


@app.route('/api/data/getAllJobs', methods =['GET'])
def get_all_jobs():
    all_jobs = JobPost.query.all()
    if all_jobs is None:
        return "No jobs you wanker"
    return jsonify([job.serialize() for job in all_jobs])
