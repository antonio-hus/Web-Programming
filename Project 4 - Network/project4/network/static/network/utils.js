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

        // Adding post content
        const contentElement = document.createElement('p');
        contentElement.textContent = post.body;

        // Adding timestamp
        const timeStampElement = document.createElement('span');
        timeStampElement.textContent = post.timestamp;

        // Adding likes count
        const likesCountElement = document.createElement('p');
        likesCountElement.textContent = "❤️ ️" + post.likesCount;

        // Adding all elements to the post container
        postElement.appendChild(userElement);
        postElement.appendChild(contentElement);
        postElement.appendChild(timeStampElement);
        postElement.appendChild(likesCountElement);

        // Adding the new post to the posts container
        postsContainer.appendChild(postElement);
    });
}
