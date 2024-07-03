// This module defines Home Page Behaviour
// Page Loaded Event
document.addEventListener('DOMContentLoaded', ()=>{

    // Initial page number
    let currentPage = 1;

    // Loading All Posts Screen on Home Page
    load_all_posts();

    // Event listener for previous page button
    const previousPageButton = document.getElementById('previous-page');
    previousPageButton.addEventListener('click', () => {
        if (currentPage > 1) {
            currentPage--;
            load_all_posts(currentPage);
        }
    });

    // Event listener for next page button
    const nextPageButton = document.getElementById('next-page');
    nextPageButton.addEventListener('click', () => {
        currentPage++;
        load_all_posts(currentPage);
    });
});

function load_all_posts(pageNumber) {

   // Fetching all posts
   fetch(`/get_all_posts/?page=${pageNumber}`)
       .then(response => response.json())
       .then(data => {
            // Creating a container for the posts
            const postsContainer = document.getElementById('all-posts');
            postsContainer.innerHTML = '';

            // Loading posts
            load_post_data(data.posts,postsContainer);

            // Update pagination controls based on pagination info
            updatePaginationControls(data.pagination);
       })

       // Error fetching data
       .catch(error => console.log("Error fetching posts:", error))
}