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
  document.querySelector('#email-view').style.display = 'none';
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
  document.querySelector('#email-view').style.display = 'none';
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

      email_block.addEventListener('click', () => load_email(email.id, mailbox))
      email.read?email_block.className = 'email-preview-read':email_block.className = 'email-preview-unread';

      document.querySelector('#emails-view').append(email_block);
    });
  });
}

function archive_mail(email_id, direction){
  // Direction is True means we archive
  // Otherwise un-archive
  fetch(`/emails/${email_id}`, {method:'PUT', body:JSON.stringify({archived:direction})})
  .then(response => {
    if (response.ok) {
      // If successful, reload the mailbox content
      if (direction) {
        // If direction is true (archive), reload the inbox
        load_mailbox('inbox');
      } else {
        // If direction is false (unarchive), reload the archive
        load_mailbox('inbox');
      }
    } else {
      console.error('Error archiving email:', response.statusText);
    }
  })
  .catch(error => {
    console.error('Network error:', error);
  });

  // Loading the inbox
  load_mailbox('inbox')
}

function load_email(email_id, mailbox){

  // Clear the email view
  document.querySelector('#email-view').innerHTML = '';

  // Show the email and hide other views
  document.querySelector('#email-view').style.display = 'block';
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';

  // Fetch the Email Data
  fetch(`/emails/${email_id}`)
  .then(response => response.json())
  .then(email => {

    // Defining HTML Elements
    const email_block = document.createElement('div');
    const header_container = document.createElement('div');
    const body_container = document.createElement('div');
    const button_container = document.createElement('div');
    const separator = document.createElement('hr');

    const sender = document.createElement('div');
    const recipients = document.createElement('div');
    const subject = document.createElement('div');
    const timestamp = document.createElement('div');
    const reply_button = document.createElement('button');

    const body = document.createElement('div');

    // Initializing HTML Elements
    sender.innerHTML = `<strong>From:</strong> ${email.sender}`;
    recipients.innerHTML = `<strong>To:</strong> ${email.recipients}`;
    subject.innerHTML = `<strong>Subject:</strong> ${email.subject}`;
    timestamp.innerHTML = `<strong>Timestamp:</strong> ${email.timestamp}`;
    body.innerHTML = `${email.body}`;
    reply_button.innerHTML = 'Reply';
    reply_button.className = "btn btn-sm btn-outline-primary";

    // Archived / Unarchived Button Logic
    const archive_button = document.createElement('button');
    archive_button.className = "btn btn-sm btn-outline-primary";
    archive_button.style.marginRight = '5px';
    if(mailbox==='inbox'){
      archive_button.innerHTML = 'Archive';
      archive_button.addEventListener('click', () => {archive_mail(email.id, true)})
      button_container.appendChild(archive_button);
    }else if(mailbox==='archive'){
      archive_button.innerHTML = 'Unarchive';
      archive_button.addEventListener('click', () => {archive_mail(email.id, false)})
      button_container.appendChild(archive_button);
    }

    // Structuring HTML Elements
    button_container.appendChild(reply_button);
    header_container.appendChild(sender);
    header_container.appendChild(recipients);
    header_container.appendChild(subject);
    header_container.appendChild(timestamp);
    header_container.appendChild(button_container);
    body_container.appendChild(body);
    email_block.appendChild(header_container);
    email_block.appendChild(separator);
    email_block.appendChild(body_container);

    fetch(`/emails/${email.id}`, {
      method: 'PUT',
      body: JSON.stringify({
          read: true
      })
    })

    // Add to Main Body HTML
    document.querySelector('#email-view').append(email_block);
  });

}