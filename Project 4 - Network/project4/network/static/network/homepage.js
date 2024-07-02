// This module defines Home Page Behaviour
// Page Loaded Event
document.addEventListener('DOMContentLoaded', ()=>{

    // Loading All Posts Screen on Home Page
    load_all_posts()
});

function load_all_posts() {

   // Fetching all posts
   fetch('/get_all_posts/')
       .then(response => response.json())
       .then(data => {

            // Creating a container for the posts
            const postsContainer = document.getElementById('all-posts');
            postsContainer.innerHTML = '';

            // Loading posts
            load_post_data(data,postsContainer);
       })

       // Error fetching data
       .catch(error => console.log("Error fetching posts:", error))
}