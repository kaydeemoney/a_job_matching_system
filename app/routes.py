from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_user, logout_user, login_required, current_user
from .models import User, Job, Application
from . import db
from werkzeug.utils import secure_filename
import os

home = Blueprint('home', __name__)

@home.route('/')
def index():
    return render_template('home.html')

@home.route('/employer_register', methods=['GET', 'POST'])
def employer_register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username=username, password=password, user_type='recruiter')
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('home.employer_dashboard'))
    return render_template('employer_register.html')

@home.route('/seeker_register', methods=['GET', 'POST'])
def seeker_register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username=username, password=password, user_type='seeker')
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('home.seeker_dashboard'))
    return render_template('seeker_register.html')

@home.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        user_role = user.user_type
        if user and user_role == "recruiter":
            login_user(user)
            return redirect(url_for('home.employer_dashboard'))
        elif user and user_role == "seeker":
            login_user(user)
            return redirect(url_for('home.seeker_dashboard'))
        else:
            return redirect(url_for('home.login'))
    return render_template('login.html')

@home.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home.index'))

@home.route('/list_job', methods=['GET', 'POST'])
@login_required
def list_job():
    if current_user.user_type != 'recruiter':
        return redirect(url_for('home.seeker_dashboard'))
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        degree = request.form['degree']
        experience = request.form['experience']
        tech_skills = request.form['tech_skills']
        soft_skills = request.form['soft_skills']
        teamwork = bool(request.form.get('teamwork'))
        cv_required = bool(request.form.get('cv_required'))
        salary_range = request.form['salary_range']
        role = request.form['role']
        job = Job(recruiter_id=current_user.id, title=title, description=description, degree=degree,
                  experience=experience, tech_skills=tech_skills, soft_skills=soft_skills, teamwork=teamwork,
                  cv_required=cv_required, salary_range=salary_range, role=role)
        db.session.add(job)
        db.session.commit()
        return redirect(url_for('home.employer_dashboard'))
    return render_template('list_job.html')

@home.route('/job_requirements/<int:job_id>', methods=['GET', 'POST'])
@login_required
def job_requirements(job_id):
    job = Job.query.get_or_404(job_id)
    if request.method == 'POST':
        academic_qual = request.form['academic_qual']
        work_experience = request.form['work_experience']
        apply_letter = request.form['apply_letter']
        tech_skills = request.form['tech_skills']
        soft_skills = request.form['soft_skills']
        tma = 'tma' in request.form
        cv = 'cv' in request.form
        asking_salary = request.form['asking_salary']

        # Handle file upload
        file = request.files['cv_file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
        else:
            return "Invalid file type"

        new_application = Application(
            job_id=job_id,
            seeker_id=current_user.id,
            academic_qual=academic_qual,
            work_experience=work_experience,
            apply_letter=apply_letter,
            tech_skills=tech_skills,
            soft_skills=soft_skills,
            tma=tma,
            cv=cv,
            asking_salary=asking_salary,
            cv_filename=filename
        )
        db.session.add(new_application)
        db.session.commit()

        return redirect(url_for('home.seeker_dashboard'))
    
    return render_template('job_requirements.html', job=job)



@home.route('/employer_dashboard')
@login_required
def employer_dashboard():
    posted_jobs = Job.query.filter_by(recruiter_id=current_user.id).all()
    return render_template('employer_dashboard.html', posted_jobs=posted_jobs)

@home.route('/seeker_dashboard')
@login_required
def seeker_dashboard():
    if current_user.user_type != 'seeker':
        return redirect(url_for('home.employer_dashboard'))
    
    available_jobs = Job.query.all()
    user_applications = Application.query.filter_by(seeker_id=current_user.id).all()

    # Fetch job information for each application
    for application in user_applications:
        job = Job.query.get(application.job_id)
        application.job = job  # Attach job object to application

    return render_template('seeker_dashboard.html', available_jobs=available_jobs, user_applications=user_applications)

@home.route('/apply/<int:job_id>', methods=['GET', 'POST'])
@login_required
def apply(job_id):
    # Fetch the job with the given job_id
    job = Job.query.get_or_404(job_id)
    if request.method == 'POST':
        # Create an Application object with job details and current user id
        application = Application(
            job_id=job.id, 
            title=job.title, 
            description=job.description, 
            degree=job.degree, 
            experience=job.experience, 
            tech_skills=job.tech_skills,
            soft_skills=job.soft_skills, 
            teamwork=job.teamwork, 
            cv_required=job.cv_required,
            salary_range=job.salary_range, 
            role=job.role, 
            seeker_id=current_user.id
        )
    # Render the apply.html template with job details and additional text variables
    return render_template('apply.html', job=job, job_id=job_id)


@home.route('/seeker_apply_view/<int:job_id>', methods=['GET', 'POST'])
@login_required
def seeker_apply_view(job_id):
    seeker_id=current_user.id
    job = Job.query.get_or_404(job_id)
    available_jobs=Job.query.all()
    job_id=job_id
    job_title=job.title
    if request.method == 'POST':
        apply_letter = request.form['apply_letter']
        academic_qual = request.form['academic_qual']
        work_experience = request.form['work_experience']
        tech_skills = request.form['tech_skills']
        soft_skills = request.form['soft_skills']
        tma = (request.form.get('tma'))
        cv = 1
        asking_salary = request.form['asking_salary']
        status="unreviewed"
        invite_details="none yet"
        application = Application(job_id=job.id, job_title=job_title, seeker_id=current_user.id, status=status,
         invite_details=invite_details, academic_qual=academic_qual, work_experience=work_experience,
         apply_letter=apply_letter, tech_skills=tech_skills, soft_skills=soft_skills, tma= tma, cv=cv, 
         asking_salary=asking_salary)
        db.session.add(application)
        db.session.commit()

    
        return redirect(url_for('home.seeker_dashboard'))
    return render_template('seeker_apply_view.html')




@home.route('/delete_job/<int:job_id>', methods=['POST'])
@login_required
def delete_job(job_id):
    job = Job.query.get_or_404(job_id)
    if current_user.id != job.recruiter_id:
        flash('You do not have permission to delete this job.', 'danger')
        return redirect(url_for('home.employer_dashboard'))
    
    # Delete all applications associated with the job
    applications = Application.query.filter_by(job_id=job_id).all()
    for application in applications:
        db.session.delete(application)
    
    # Delete the job
    db.session.delete(job)
    db.session.commit()
    
    flash('Job and associated applications deleted successfully!', 'success')
    return redirect(url_for('home.employer_dashboard'))


@home.route('/job_applicants/<int:job_id>')
@login_required
def job_applicants(job_id):
    job = Job.query.get_or_404(job_id)
    applicants = job.applicants  # Assuming a relationship is defined in the Job model
    return render_template('job_applicants.html', job=job, applicants=applicants)



# Helper function to check allowed file extensions
def allowed_file(filename):
    allowed_extensions = {'pdf'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions



@home.route('/view_applicants')
@login_required
def view_applicants():
    applications = Application.query.all()
    return render_template('view_applicants.html', applications=applications)
