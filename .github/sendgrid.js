#! /usr/bin/env node

const sgMail = require('@sendgrid/mail');
sgMail.setApiKey(process.env.SENDGRID_API_KEY);

const fs = require('fs'),
    filename = 'README.md',
    fileType = 'text/plain',
    data = fs.readFileSync('./README.md');

const msg = {
    to: ['devarshi.j.raval@gmail.com'],
    from: {
        name: 'Competitive Tracker',
        email: 'devarshi.j.raval@gmail.com'
    },
    subject: 'Rate Scanner Release',
    text: 'Hello, PFA the latest Rate Scanner sheet.',
    attachments: [
        {
            content: data.toString('base64'),
            filename: filename,
            type: fileType,
            disposition: 'attachment',
        },
    ],
};

sgMail
    .send(msg)
    .then(() => console.log('Mail sent successfully'))
    .catch(error => console.error(error.toString()));
