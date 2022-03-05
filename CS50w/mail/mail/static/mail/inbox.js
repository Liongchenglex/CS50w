document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector("#compose-form").addEventListener("submit", send_email);

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
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // load appropriate mailbox
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    // to assist with debugs
    console.log(emails);

    // loop through each email
    emails.forEach(email => {
      const element = document.createElement('div');
      make_preview(email, element, mailbox);

      // styling css of each email
      element.style.borderBottom= 'solid 2px white';
      element.style.padding = '5px';

      // add hover effect
      element.addEventListener('mouseover', () => 
        element.style.background = 'lightblue');
      if (email['read']){
        element.addEventListener('mouseout', () =>
          element.style.background = 'lightgrey');
      } else{
        element.addEventListener('mouseout', () =>
          element.style.background = 'white');
      }

      // Isolate individual email
      element.addEventListener('click', () => 
        view_email(email['id'], mailbox));

      // add element to html
      document.querySelector('#emails-view').append(element)
    });

  })
  .catch(error => console.log(error));
}

function make_preview(email, element, mailbox){
  // creating divs
  // const creator = document.createElement('div');      ======      if want to make it one line
  const people = document.createElement('div');
  const subject_line = document.createElement('div');
  const timestamp = document.createElement('div');

  // different templates depending on mailbox
  if (mailbox === 'sent')
  {
    const recipients = email['recipients'].join(", ") + " ";
    people.innerHTML = `To: ${recipients}`;
  }
  else 
  {
    const sender = email['sender'] + ' ';
    people.innerHTML = `From: <strong>${sender} </strong>`;
  }

  element.append(people);

  //  ================= to make the div one line ============= \\
  // creator.append(people);
  // creator.innerHTML += email['subject']
  // element.append(creator);

  // displaying subject line
  subject_line.innerHTML = `Subject: ${email['subject']}`;
  element.append(subject_line);

  // displaying timestamp
  timestamp.innerHTML = email['timestamp'];
  timestamp.style.color = 'grey';
  timestamp.style.textAlign = 'end';
  element.append(timestamp)

  // change color to grey if read
  if (email['read']){
    element.style.background = 'lightgrey';
  }

}



function view_email(email_id, mailbox){
  // to assist with debugs
  console.log(mailbox);

  // fetch api
  fetch(`/emails/${email_id}`)
  .then(response => response.json())
  .then(email => {
    const parent = document.createElement('div');
    make_email(parent, email, mailbox);
    document.querySelector('#email-view').append(parent)
    
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#email-view').style.display = 'block';
    document.querySelector('#compose-view').style.display = 'none';

  })
  .catch(error => console.log(error));
}



function make_email(parent, email, mailbox){
  // erase existing email-view
  document.querySelector('#email-view').innerHTML = '';

  // creating divs for sender, recripients, subject, timestamp and body
  const buttons = document.createElement('div');
  const heading = document.createElement('div');
  const sender = document.createElement('div');
  const recipients = document.createElement('div');
  const subject = document.createElement('div');
  const timestamp = document.createElement('div');
  const body = document.createElement('div');
  const reply = document.createElement('button');
  const back = document.createElement('button');

  // fill HTML for sender
  sender_info = email['sender'] + ' ';
  sender.innerHTML = `<strong>From</strong>: ${sender_info}`;
  heading.append(sender);

  // fill HTML for recipients
  recipients_info = email['recipients'].join(", ") + " ";
  recipients.innerHTML = `<strong>To</strong>: ${recipients_info}`;
  heading.append(recipients);

  // fill HTML for subject
  subject.innerHTML = `<strong>Subject</strong>: ${email['subject']}`;
  heading.append(subject);

  // fill HTML for timestamp
  timestamp.innerHTML = `<strong>Timestamp</strong>: ${email['timestamp']}`;
  heading.append(timestamp);

  // make button to reply
  reply.innerHTML = 'Reply';
  reply.className = "btn-primary m-1";
  reply.addEventListener('click', function(){
    // load the compose email page
    compose_email();
    // prefill the compose email form
    document.querySelector('#compose-recipients').value = email['sender'];
    if (email['subject'].slice(0,3) !== 'Re:'){
      document.querySelector('#compose-subject').value = `Re: ${email['subject']}`;
    } else{
      document.querySelector('#compose-subject').value = email['subject'];
    }
    let details = `------------ On ${email['timestamp']} ${email['sender']} wrote: ------------`;
    let prefilled = '\n' + '\n' + details +'\n';
    document.querySelector('#compose-body').value = prefilled + '\n' + email['body']; 
  });
  heading.append(reply);

  // make button to archive
  if (mailbox === 'inbox' || mailbox === 'archive'){
    // to assist in debugs
    console.log('it worked');
    // create archive button
    const archive = document.createElement('button');
    archive.className = "btn-primary m-1";
    // set the button depending on archive or unarchive
    archive.innerHTML = email['archived'] ? 'Unarchive' : 'Archive';
    // arvhice email when clicked
    archive.addEventListener('click', function(){
        archive_email(email);
    });
    heading.append(archive);
  }

  // style and add the headings
  heading.style.borderBottom = ' 1px solid grey ';
  parent.append(heading);

  // add content of the body
  console.log(email['body']);
  let value = email['body'].replaceAll('\n' ,'<br/>' )
  body.innerHTML = `<p class="m-2">${value}</p>`;
  parent.append(body);
  
  // back button
  let buttonText = mailbox;
  if (mailbox === 'archive'){
    buttonText = 'Archived';
  } else{
    buttonText = `${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}`
  }
  back.innerHTML = `Back to ${buttonText}`;
  back.className = "btn-primary m-1";
  back.addEventListener('click', () => load_mailbox(mailbox));
  parent.append(back);

  // setting read
  fetch(`/emails/${email['id']}`, {
    method: 'PUT',
    body: JSON.stringify({
      read : true
    })
  });
}


// archiving emails with PUT
function archive_email(email){
  if(email['archived'] === false ){
    console.log(email['archived']);
    fetch(`/emails/${email['id']}`, {
    method: 'PUT',
    body: JSON.stringify({
        archived: true
      })
    })
    .then(result => console.log(result['archived']))
    .then (result => load_mailbox('inbox'));
  }else{
    fetch(`/emails/${email['id']}`, {
      method: 'PUT',
      body: JSON.stringify({
          archived: false
      })
    })
    .then(result => load_mailbox('inbox'));  
  }
}


// sending email
function send_email() {
  event.preventDefault();
  const recipients = document.querySelector("#compose-recipients").value;
  const subject = document.querySelector("#compose-subject").value;
  const body = document.querySelector("#compose-body").value;
 
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
      recipients: recipients,
      subject: subject,
      body : body,
    })
  })
  // convert response to json 
  .then (response => response.json())

  // test result and load sent mailbox
  .then (result => {
    console.log(result);
    load_mailbox('sent');
  })

  // error handling
  .catch((error) => console.log(error));
}

