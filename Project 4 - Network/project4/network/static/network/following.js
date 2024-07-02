// This module defines Following Posts Page Behaviour
// Page Loaded Event
document.addEventListener('DOMContentLoaded', ()=>{

    // Loading Following User's Posts Screen on Following Page
    load_following_posts()
});

function load_following_posts()
{

   // Fetching following posts
   fetch('/get_following_posts/')
       .then(response => response.json())
       .then(data => {

            // Creating a container for the posts
            const postsContainer = document.getElementById('following-posts');
            postsContainer.innerHTML = '';

            // Loading posts
            load_post_data(data,postsContainer);
       })

       // Error fetching data
       .catch(error => console.log("Error fetching posts:", error))
}