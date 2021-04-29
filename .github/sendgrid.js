#! /usr/bin/env node

const sgMail = require('@sendgrid/mail');
sgMail.setApiKey(process.env.SENDGRID_API_KEY);

const fs = require('fs'),
    filename = 'RateScanner.xlsx',
    fileType = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    data = fs.readFileSync('./RateScanner.xlsx');

const msg = {
    to: ['devarshi.j.raval@gmail.com'],
    from: {
        name: 'Competitive Tracker',
        email: 'devarshi.j.raval@gmail.com'
    },
    subject: 'Rate Scanner Release',
    text: 'Hello, PFA the latest Rate Scanner sheet.',
    //html: '<p>Hello HTML world!</p>',
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