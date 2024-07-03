// This module defines commonly used operations
// Load post data into a given container
function load_post_data(data, postsContainer) {
    // Adding data to the posts container
    data.forEach(post => {

        // Creating a container for individual post
        const postElement = document.createElement('div');
        postElement.className = 'post';

        // Adding owner username
        const userElement = document.createElement('h5');

        // Creating the anchor tag
        const userLink = document.createElement('a');
        userLink.href = `/users/${encodeURIComponent(post.owner)}`;
        userLink.textContent = post.owner;

        // Append the anchor to the h5 element
        userElement.appendChild(userLink);
        postElement.appendChild(userElement);

        // Adding timestamp
        const timeStampElement = document.createElement('span');
        timeStampElement.textContent = post.timestamp;
        postElement.appendChild(timeStampElement);

        // Adding likes count
        if(post.is_authenticated) {
            const likesCountElement = document.createElement('p');
            if (post.is_liked) {
                likesCountElement.textContent = "🤍 ️" + post.likesCount;
            } else {
                likesCountElement.textContent = "❤️ ️" + post.likesCount;
            }
            likesCountElement.style.cursor = "pointer";
            likesCountElement.addEventListener('click', () => {

                const csrfToken = getCookie('csrftoken');

                // Post was already liked => Unlike
                if (post.is_liked) {

                    // Front-End Update
                    post.likesCount -= 1
                    likesCountElement.textContent = "❤️ ️" + (post.likesCount);
                    post.is_liked = false;

                    // Back-End Update
                    fetch(`/update_post/`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': csrfToken,  // Ensure CSRF token is included
                        },
                        body: JSON.stringify({
                            "post_id": post.id,
                            "owner": post.owner,
                            "content": post.body,
                            "likes": post.likesCount - 1
                        }),
                    })
                        .then(response => response.json())
                        .then(data => {
                            if (data.status === "success") {
                                console.log("Update Post Action Worked")
                            } else {
                                console.error("Update Post Action Failed");
                            }
                        })
                        .catch(error => {
                            console.error("Error occurred updating post:", error);
                        });
                }

                // Post was not already liked => Like
                else {

                    // Front-End Update
                    post.likesCount += 1
                    likesCountElement.textContent = "🤍 ️ ️" + (post.likesCount);
                    post.is_liked = true;

                    // Back-End Update
                    fetch(`/update_post/`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': csrfToken,  // Ensure CSRF token is included
                        },
                        body: JSON.stringify({
                            "post_id": post.id,
                            "owner": post.owner,
                            "content": post.body,
                            "likes": post.likesCount + 1
                        }),
                    })
                        .then(response => response.json())
                        .then(data => {
                            if (data.status === "success") {
                                console.log("Update Post Action Worked")
                            } else {
                                console.error("Update Post Action Failed");
                            }
                        })
                        .catch(error => {
                            console.error("Error occurred updating post:", error);
                        });
                }
            });
            postElement.appendChild(likesCountElement);
        }

        // Adding post content
        const contentElement = document.createElement('p');
        contentElement.textContent = post.body;
        postElement.appendChild(contentElement);

        // Create Edit Form
        if(post.is_owner) {
            const editBox = document.createElement('textarea');
            editBox.textContent = contentElement.textContent;
            editBox.className = 'form-control';
            editBox.hidden = true;
            postElement.appendChild(editBox);

            const submitEditButton = document.createElement('button');
            submitEditButton.className = 'btn btn-primary';
            submitEditButton.textContent = 'Save';
            submitEditButton.hidden = true;
            postElement.appendChild(submitEditButton);

            submitEditButton.addEventListener('click', () => {
                editBox.hidden = true;
                submitEditButton.hidden = true;

                // Updating the post's text ( Front-End )
                contentElement.textContent = editBox.value;

                // Updating the post's text ( Back-End )
                const csrfToken = getCookie('csrftoken');
                fetch(`/update_post/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrfToken,  // Ensure CSRF token is included
                    },
                    body: JSON.stringify({ "post_id": post.id, "owner": post.owner, "content": editBox.value, "likes": post.likesCount }),
                })
                .then(response => response.json())
                .then(data => {
                    if (data.status === "success") {
                        console.log("Update Post Action Worked")
                    } else {
                        console.error("Update Post Action Failed");
                    }
                })
                .catch(error => {
                    console.error("Error occurred updating post:", error);
                });

                contentElement.hidden = false;
                editElement.hidden = false;
            });

            // Create Edit Button
            const editElement = document.createElement('span');
            editElement.textContent = "Edit";
            editElement.classList.add("text-primary");
            editElement.style.textDecoration = "underline";
            editElement.style.cursor = "pointer";

            editElement.addEventListener('click', () => {
                contentElement.hidden = true;
                editElement.hidden = true;
                editBox.hidden = false;
                submitEditButton.hidden = false;
            });

            postElement.appendChild(editElement);
        }

        // Adding the new post to the posts container
        postsContainer.appendChild(postElement);
    });
}

// Function to update pagination controls based on pagination information
function updatePaginationControls(paginationInfo) {
    const previousPageButton = document.getElementById('previous-page');
    const nextPageButton = document.getElementById('next-page');

    // Enable/disable previous page button based on pagination info
    if (paginationInfo.has_previous) {
        previousPageButton.classList.remove('disabled');
        previousPageButton.querySelector('.page-link').setAttribute('tabindex', '0');
    } else {
        previousPageButton.classList.add('disabled');
        previousPageButton.querySelector('.page-link').setAttribute('tabindex', '-1');
    }

    // Enable/disable next page button based on pagination info
    if (paginationInfo.has_next) {
        nextPageButton.classList.remove('disabled');
        nextPageButton.querySelector('.page-link').setAttribute('tabindex', '0');
    } else {
        nextPageButton.classList.add('disabled');
        nextPageButton.querySelector('.page-link').setAttribute('tabindex', '-1');
    }
}

// Function for getting Cookie Information
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