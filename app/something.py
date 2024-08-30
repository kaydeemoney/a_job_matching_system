if the recruiter login is successful:
    section A:
    @there should be a button to list a new job (which is working already)
    @there should be a div to list posted jobs in a structured way in the format (job_name, delete , view_more)
    @ once a job is deleted, every job id in the qualifications column associated with the said job will be removed
    if view more is clicked:
        @ it should list out every job seeker name that applied with a link to view details
        if this link is clicked:
            @ he should be able to check the application letter of the seeker
            @ there should be a link to view the cv of the seeker (which is in pdf format)
            @ there should be an accept button and a decline button which will update the job applications table as "accepted", "denied" or leave it as "not viweed yet"
            @ there should be an optional "extra comment" text box that will enter the "invite_details" column in the job applications table 
        if this link hasnt been reached yet, the job request status should be "no view yet"

@ in the job qualifications table, the strict naming of this table are as follows:
@ tablename  =applications
table column details are	id	job_id	seeker_id	status	invite_details
@ in this pseudocode, for the above are used loosely	status is loosely called request_status, invite_details is loosely called job comment status


if the job_seeker login is successful,
he will be able to see available jobs from activities of recruiters from section A with a link to view more
if this view more link is clicked:
    @ it will show all the details posted by the recruiter
    @ there will be a "click this if you are interested link"
    if he is interested:
        @there will be a link to apply which will take him to a page to apply
        if he is in the page to aply:
            @there will be a text box that will contain the application letter
            @ there will be an upload cv button that successfully uploads the cv and put it in a folder where 
            the recruiter can view it in section A above
            @ then there will be a submit button
there should also be a section or div still in this page for "jobs applied for" names and a link to view more using the job_id to link each user to the jobs they applied for
the view more link in this page will link to a page in which these details will display:
-job details from section A
- the job status gotten from the applications table
the comment gotten from the recruiter




@a lower div with the title jobs applied will display all the jobs each user applied for in the format
job_id, job name, recruiter name, request status, job comment status