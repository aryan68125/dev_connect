#this file takes care of pagination in projects_list.html page

#paginators import it will allow us to create a multi page website
#PageNotAnInteger, EmptyPage will allow us to set the page number to 1 when the user first go to our projects page
#in other words page 1 will be shown to the user when he/she opens up the project_list.html page for the first time
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def paginate_projects_list(request, projects, results):
            #PAGE PAGINATION STARTS HERE-----------------------------------------------------
            #setting up the pages in our project_list.html page
            #request.GET.get('page') will get the page number that we are currently on from the frontend
            page = request.GET.get('page') #give us the first page of these results
            results = 6 #give us 6 projects(results) per page
            paginator = Paginator(projects, results) #paginator = Paginator(query set , results ) go ahead an paginate the project query set and give us the results here

            try:
                #now paginate the project list page
                #now reset the projects variable and index it by a specific page only get 6 results (projects)
                #here we are defining what page do we wanna get from this query set
                #so here we will be getting 6 projects and we are gonna get the first page those 6 projects
                projects = paginator.page(page)
            #the page will not be passed in when the user first enters the projects_list page
            except PageNotAnInteger: #if page is not passed in then it will come to this block
                page=1
                projects = paginator.page(page)
            #if user tries to go to a page number that does not exists using url links in the browser then we should prevent our website from crashing
            #paginator.num_pages will tell us how many pages we have
            except EmptyPage:
                page = paginator.num_pages #if the user goes out of bounds or exceeds the max number of pages that are actually present in the project_list.html page then go ahead and give us the last page
                projects = paginator.page(page)

            #right now in this current state pagination will produce 100 buttons if qwe have 100 pages in our website but we don't want that
            #we want to limit the number of buttons shown at the bottom of the page to 5 so we need to somehow create a range or rolling window for our page button in pagination

            leftIndex = int(page) - 2 #the page that is on our left side
            #leftIndex is gonna return -ve if we are on page 3 as you know 3-4=-1 so we need to avoid that from happening
            if leftIndex < 1:
                leftIndex = 1

            rightIndex = int(page) + 3 #far right page
            #here we need to avoid creating extra buttons for next page if we are already at the last page here let me give an example
            #if a user is at page 15 and 15th page is the last page then we should avoid making more page buttons from 15 to 20
            #as 16 to 20 page do not exist in this senario so we need to avoid this
            if rightIndex > paginator.num_pages:
                rightIndex = paginator.num_pages +1

            custom_range = range(leftIndex,rightIndex)
            #PAGE PAGINATION ENDS HERE-------------------------------------------------------------------------------------------------------

            return custom_range, projects
