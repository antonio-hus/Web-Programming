document.addEventListener("DOMContentLoaded", () => {

    // Load Profile on visit
    const userProfileElement = document.querySelector('#user-page');
    const username = userProfileElement.dataset.username;
    if (username) {
        load_profile(username);
    }

});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function load_profile(username)
{

    // Fetching user data
    fetch(`/get_user/${encodeURIComponent(username)}`)
    .then(response => response.json())
    .then(data => {

        // Selecting the user page container
        const userProfileElement = document.querySelector('#user-page');

        // Clear any existing content inside the user page container
        userProfileElement.innerHTML = '';

        // Creating the Header container
        const userHeaderBox = document.createElement('div');
        userHeaderBox.id = 'user-header';

        // Creating username label
        const userUsername = document.createElement('h4');
        userUsername.textContent = data.username;
        userHeaderBox.appendChild(userUsername);

        // Creating follower / following count container & labels
        const userFollowCountBox = document.createElement('div');
        userFollowCountBox.id = 'user-follow-box';

        const userFollowers = document.createElement('span');
        userFollowers.textContent = `Followers: ${data.followerCount}`;
        userFollowers.classList.add('mr-3');
        userFollowers.id = "user-followers"

        const userFollowing = document.createElement('span');
        userFollowing.textContent = `Following: ${data.followingCount}`;

        userFollowCountBox.appendChild(userFollowers);
        userFollowCountBox.appendChild(userFollowing);

        // Appending follower / following count box to header
        userHeaderBox.appendChild(userFollowCountBox);

        // Creating follow / unfollow button
        // Only available to authenticated, non-owner users
        if (data.is_authenticated && !data.is_owner) {

            // Creating button
            const userFollowButton = document.createElement('button');

            // Checking the user's relation to the other
            // Not following => Follow
            if (!data.is_following) {
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
        data.posts.forEach(post => {
            // Creating a container for individual post
            const postElement = document.createElement('div');
            postElement.className = 'post';

            // Adding owner username
            const userElement = document.createElement('h5');
            userElement.textContent = post.owner;

            // Adding post content
            const contentElement = document.createElement('p');
            contentElement.textContent = post.body;

            // Adding timestamp
            const timeStampElement = document.createElement('span');
            timeStampElement.textContent = post.timestamp;

            // Adding likes count
            const likesCountElement = document.createElement('p');
            likesCountElement.textContent = `❤️ ${post.likesCount}`;

            // Appending elements to post container
            postElement.appendChild(userElement);
            postElement.appendChild(contentElement);
            postElement.appendChild(timeStampElement);
            postElement.appendChild(likesCountElement);

            // Appending post container to user body box
            userBodyBox.appendChild(postElement);
        });

        // Appending user body box to user page container
        userProfileElement.appendChild(userBodyBox);
    })
    .catch(error => console.log("There was an error fetching data" + error));

}