// This module defines User Profile Page Behaviour
// Page Loaded Event
document.addEventListener("DOMContentLoaded", () => {

    // Initial page number
    let currentPage = 1;

    // Load Profile on visit
    const userProfileElement = document.querySelector('#user-page');
    const username = userProfileElement.dataset.username;
    if (username) {
        load_profile(username, currentPage);
    }

    const previousPageButton = document.getElementById('previous-page');
    previousPageButton.addEventListener('click', () => {
        if (currentPage > 1) {
            currentPage--;
            load_profile(username, currentPage);
        }
    });

    // Event listener for next page button
    const nextPageButton = document.getElementById('next-page');
    nextPageButton.addEventListener('click', () => {
        currentPage++;
        load_profile(username, currentPage);
    });

});

// Loading the user's profile
function load_profile(username, pageNumber)
{

    // Fetching user data
    fetch(`/get_user/${encodeURIComponent(username)}/?page=${pageNumber}`)
    .then(response => response.json())
    .then(data => {

        console.log(data);

        // Selecting the user page container
        const userProfileElement = document.querySelector('#user-page');

        // Clear any existing content inside the user page container
        userProfileElement.innerHTML = '';

        // Creating the Header container
        const userHeaderBox = document.createElement('div');
        userHeaderBox.id = 'user-header';

        // Creating username label
        const userUsername = document.createElement('h4');
        userUsername.textContent = data.user_data.username;
        userHeaderBox.appendChild(userUsername);

        // Creating follower / following count container & labels
        const userFollowCountBox = document.createElement('div');
        userFollowCountBox.id = 'user-follow-box';

        const userFollowers = document.createElement('span');
        userFollowers.textContent = `Followers: ${data.user_data.followerCount}`;
        userFollowers.classList.add('mr-3');
        userFollowers.id = "user-followers"

        const userFollowing = document.createElement('span');
        userFollowing.textContent = `Following: ${data.user_data.followingCount}`;

        userFollowCountBox.appendChild(userFollowers);
        userFollowCountBox.appendChild(userFollowing);

        // Appending follower / following count box to header
        userHeaderBox.appendChild(userFollowCountBox);

        // Creating follow / unfollow button
        // Only available to authenticated, non-owner users
        if (data.user_data.is_authenticated && !data.user_data.is_owner) {

            // Creating button
            const userFollowButton = document.createElement('button');

            // Checking the user's relation to the other
            // Not following => Follow
            if (!data.user_data.is_following) {
                userFollowButton.textContent = 'Follow';
                userFollowButton.className = 'btn btn-primary';
            } else {
                // Following => Unfollow
                userFollowButton.textContent = 'Unfollow';
                userFollowButton.className = 'btn btn-secondary';
            }

            // Adding event listener to follow/unfollow button
            userFollowButton.addEventListener('click', () => {
                const csrfToken = getCookie('csrftoken');
                fetch(`/follow_user/${encodeURIComponent(username)}/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrfToken,  // Ensure CSRF token is included
                    },
                    body: JSON.stringify({ username: username }),
                })
                .then(response => response.json())
                .then(data => {
                    if (data.status === "success") {
                        load_profile(username);
                    } else {
                        console.error("Follow/unfollow failed");
                    }
                })
                .catch(error => {
                    console.error("Error occurred during follow/unfollow:", error);
                });

            });

            // Adding button to follower box
            userHeaderBox.appendChild(userFollowButton);
        }

        // Appending header box to user page container
        userProfileElement.appendChild(userHeaderBox);
        userProfileElement.appendChild(document.createElement('hr'));

        // Creating the Body Container
        const userBodyBox = document.createElement('div');
        userBodyBox.id = 'user-body';

        // Adding posts to the user profile body
        load_post_data(data.user_data.posts, userBodyBox);

        // Appending user body box to user page container
        userProfileElement.appendChild(userBodyBox);

        // Update pagination controls
        updatePaginationControls(data.pagination);

    })
    .catch(error => console.log("There was an error fetching data" + error));

}
