//Link up Paginator and Search Form in developers page and projects page using javascript
//apply this javascript to the home page

let searchForm = document.getElementById("searchForm"); //get the search form from the projects_list.html page document means we are going through the entire page getElementById("searchForm = is the id of the form that we gave in the projects_list.html page")
let pageLinks =  document.getElementsByClassName("page-link"); //get all the buttons in the pagination.html via page-link button class

//if we don't have a search form then restrict this code from executing
if(searchForm)
  {
     for(let i=0; pageLinks.length> i; i++)
     {
       pageLinks[i].addEventListener('click', function (e)
       {
             e.preventDefault() //stop the default submit function from happening in the backend
             //get thedata from this page from the pagination buttons
             let page = this.dataset.page
             //add hidden search input to form
             //get the searchForm innerHTML allows us to add HTML contents
             searchForm.innerHTML += `<input value="${page}" name="page" hidden/>`
             //submit searchForm using javascript in the frontend
             searchForm.submit()
         }
       )
       }
    }

//this javascript code below will remove the tag via api from a project
    let tags = document.getElementsByClassName('project-tag')

    for (let i = 0; tags.length > i; i++) {
        tags[i].addEventListener('click', (e) => {
            let tagId = e.target.dataset.tag
            let projectId = e.target.dataset.project

            // console.log('TAG ID:', tagId)
            // console.log('PROJECT ID:', projectId)

            fetch('http://127.0.0.1:8000/api/remove-tag/', {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ 'project': projectId, 'tag': tagId })
            })
                .then(response => response.json())
                .then(data => {
                    e.target.remove()
                })

        })
    }
