// This module defines Following Posts Page Behaviour
// Page Loaded Event
document.addEventListener('DOMContentLoaded', ()=>{

    // Initial page number
    let currentPage = 1;

    // Loading Following Posts Screen on Following Page
    load_following_posts(currentPage)

    // Event listener for previous page button
    const previousPageButton = document.getElementById('previous-page');
    previousPageButton.addEventListener('click', () => {
        if (currentPage > 1) {
            currentPage--;
            load_following_posts(currentPage);
        }
    });

    // Event listener for next page button
    const nextPageButton = document.getElementById('next-page');
    nextPageButton.addEventListener('click', () => {
        currentPage++;
        load_following_posts(currentPage);
    });
});

function load_following_posts(pageNumber)
{

   // Fetching following posts
   fetch(`/get_following_posts/?page=${pageNumber}`)
       .then(response => response.json())
       .then(data => {

            // Creating a container for the posts
            const postsContainer = document.getElementById('following-posts');
            postsContainer.innerHTML = '';

            // Loading posts
            load_post_data(data.posts,postsContainer);

            // Update pagination controls based on pagination info
            updatePaginationControls(data.pagination);
       })

       // Error fetching data
       .catch(error => console.log("Error fetching posts:", error))
}