document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  // On submit, make a POST request to /emails
  document.querySelector('#compose-form').onsubmit = () => {
    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
          recipients: document.querySelector('#compose-recipients').value,
          subject: document.querySelector('#compose-subject').value,
          body: document.querySelector('#compose-body').value,
      })
    })
    .then(response => response.json())
    .then(result => {
        // Print result
        console.log(result);
    });

    // Load the 'Sent' Mailbox
    load_mailbox('sent')

    return false;
  }
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Show the mailbox content
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    emails.forEach(email => {
      const email_block = document.createElement('div');
      const left_side = document.createElement('div');
      const right_side = document.createElement('div');
      const sender = document.createElement('strong');
      const subject = document.createElement('p');
      const timestamp = document.createElement('div');
      const reply_button = document.createElement('button');

      sender.innerHTML = `${email.sender}`;
      subject.innerHTML = `${email.subject}`;
      timestamp.innerHTML = `${email.timestamp}`;
      reply_button.innerHTML = 'Reply';
      reply_button.className = "btn btn-sm btn-outline-primary";

      left_side.appendChild(sender);
      left_side.appendChild(subject);
      right_side.appendChild(timestamp);
      right_side.appendChild(reply_button);
      email_block.appendChild(left_side);
      email_block.appendChild(right_side);
      email.read?email_block.className = 'email-preview-unread':email_block.className = 'email-preview-read';

      document.querySelector('#emails-view').append(email_block);
    });
  });
}