import json, requests
from flask import render_template, flash, redirect, url_for, request, jsonify
from app import app, db
from app.forms import LoginForm, RegistrationForm, JobPostForm, EditListingForm, DeleteListingBtn, ApplyJobBtn, EditProfileForm, AcceptApplicationBtn, RejectApplicationBtn, ListingQueryForm
from flask_login import current_user, login_user, logout_user,login_required
from app.models import User, JobPost, Application
from werkzeug.urls import url_parse
from wtforms.validators import ValidationError
from sqlalchemy import func, or_
import socket

@app.route('/weisheng',methods=['GET','POST'])
def weisheng():
    messages = False
    if current_user.is_authenticated:
        return redirect(url_for('index_reg'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            # flash('Invalid username or password')
            messages = True
            return render_template('login2.html', title='Sign In', form=form, messages=messages)
        login_user(user)
        if user.role == 'regular':
            return redirect(url_for('index_reg'))
        elif user.role == 'admin':
            return redirect(url_for('index_admin'))

    return render_template('login2.html', title='Sign In', form=form)

@app.route('/weisheng2', methods=['POST'])
def weisheng2():
    not_smu_email = False
    if current_user.is_authenticated:
        return redirect(url_for('index_reg'))
    form = RegistrationForm()
    if form.validate_on_submit():
        if 'smu.edu.sg' in form.email.data:
            user = User(email=form.email.data, role='regular', stars=5, gender='')
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('weisheng'))
        else:
            not_smu_email = True
            return render_template('register2.html', title='Register', form=form, not_smu_email=not_smu_email)
    return render_template('register2.html', title='Register', form=form)



@app.route('/')
@app.route('/index_reg')
@login_required
def index_reg():
    y = 7
    x = 'hello goy'
    z = [1,2,3,4,5,6]
    return render_template('index_reg.html', y=y, x=x, z=z)


def takeSecond(elem):
    return elem[1]

@app.route('/findjobs',methods=['GET','POST'])
@login_required
def findjobs():
    form = ListingQueryForm()
    querystatus = None
    queried_jobs = None
    count = 0
    kw = []

    if form.validate_on_submit() and form.submit.data:

        if form.keyword.data is not '' and len(form.keyword.data) > 1:
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
    # print(jsonData)

    kw = jsonData['keywords']
    listing_count = jsonData['listingCount']

    if kw == []:
        data = []
        following_jobs = JobPost.query.all()
        following_jobs = following_jobs[listing_count:listing_count+5]
        # print(following_jobs)
        for job in following_jobs:
            data.append([job.id,job.title,job.organization,job.timestamp.strftime('%Y-%m-%d'),job.email])
        # print(data)
        return jsonify(success=True, data=data)

    else:
        # print(kw)
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
        print(following_jobs_temp)

        for job in following_jobs_temp:
            data.append([job[0].id,job[0].title,job[0].organization,job[0].timestamp.strftime('%Y-%m-%d'),job[0].email])

        # print(data)

        return jsonify(success=True,data=data)



@app.route('/applyjob/<id>',methods=['GET','POST'])
@login_required
def applyjob(id):
    form = ApplyJobBtn()
    job = JobPost.query.filter_by(id=id).first_or_404()
    check_appl = Application.query.filter_by(jobpost_id=job.id, user_id=current_user.id).first()
    impressions = job.impressions.split(',')
    # print(impressions)
    if str(current_user.id) not in impressions:
        job.impressions += str(current_user.id) + ','
        db.session.commit()
    # print(JobPost.query.filter_by(id=id).first().impressions)

    applied = False
    if check_appl is not None:
        applied = True

    if form.validate_on_submit():
        if check_appl is None:
            new_application = Application(jobpost_id=job.id, user_id=current_user.id, status='unread')
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


# @app.route('/morejobs',methods=['GET','POST'])
# @login_required
# def morejobs():
#     keywords = User.query.filter_by(id=current_user.id).first().keywords
#     keyword = keywords[0]
#     payload = {
#     'publisher':,
#     'v':2,
#     'userip':request.remote_addr,
#     'useragent':request.headers.get('User-Agent')
#     'q':
#     }
#
#     return headers



@app.route('/myprofile/<id>',methods=['GET','POST'])
@login_required
def myprofile(id):
    user = User.query.filter_by(id=current_user.id).first_or_404()
    form = EditProfileForm()
    comment = []
    if form.validate_on_submit() and form.submit.data:
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
            db.session.commit()
            comment.append('Changes saved successfully.')
            return render_template('myprofile.html',user=user,form=form,comment=comment)
        else:
            comment.append('Number of Keywords Exceeded')
            form.keywords.data = user.keywords
            return render_template('myprofile.html',user=user,form=form,comment=comment)

    elif request.method == 'GET':
        form.gender.data = user.gender
        form.bio.data = user.bio
        form.phone_no.data = user.phone_no
        form.keywords.data = user.keywords
    return render_template('myprofile.html',user=user,form=form,comment=comment)



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
            # print(l.impressions)
            if l.impressions != '':
                impressions_list.append(len(l.impressions.split(',')) - 1)
            else:
                impressions_list.append(0)

        # print(impressions_list)

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
            # flash('Invalid username or password')
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
            user = User(email=form.email.data, role='regular', stars=5, gender='')
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
    all_jobs = JobPost.query.filter_by(email=current_user.email).order_by(JobPost.timestamp.desc())
    errors = []
    # print(all_jobs)
    if current_user.role != 'admin':
        return 'You are not authorized to access this page.'
    else:
        if form.validate_on_submit():
            temp = form.keywords.data
            temp = temp.split(',')
            keywords = []
            for t in temp:
                keywords.append(t.strip().lower())


            if len(keywords) <= 10:
                keywords = str(','.join(keywords))
                jobpost = JobPost(email = current_user.email, title = form.title.data, organization = form.organization.data, description = form.description.data, pay = form.pay.data, pay_frequency = form.pay_frequency.data, keywords=keywords, impressions = '')
                # start_date = form.start_date.data, end_date = form.end_date.data)
                db.session.add(jobpost)
                db.session.commit()
                # return render_template('mylistings.html', form=form, all_jobs=all_jobs)
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
    if application.status == 'unread':
        application.status = 'pending'
        db.session.commit()
    if form1.validate_on_submit() and form1.submit.data:
        application.status = 'accepted'
        db.session.commit()
        return redirect(url_for('viewapplicants',id=post.id))
    elif form2.validate_on_submit() and form2.submit.data:
        application.status = 'rejected'
        db.session.commit()
        return redirect(url_for('viewapplicants',id=post.id))
    return render_template('applicantinfo.html', post=post, application=application, user=user, form1=form1, form2=form2)
