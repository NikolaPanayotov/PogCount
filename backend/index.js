// Package Requirements
const express = require('express');
const mongoose = require('mongoose');
const { EventEmitter } = require('events');

// Local Requirements
const emoteCount = require('./schemas/emotecounts');
const { Stream } = require('./helpers/stream')


// Express setup
const app = express();
const port = 3000;
app.set('view engine', 'ejs');

// Mongoose connection to DB
mongoose.connect('mongodb://mongo1:27017/pogcount', {useNewUrlParser: true, 
                                                    useUnifiedTopology: true,
                                                    // user: 'root',
                                                    // pass: 'rootpassword',
                                                    // authSource: 'admin'
                });
const db = mongoose.connection;
// Handle error/successful connections
db.on('error', console.error.bind(console, 'connection error:'));
db.once('open', () => {
    console.log('[SERVER] Database connected');
}); 

// Landing page (only planned page?)
app.get('/', async (req, res) => {
    const emotes = await emoteCount.find({})
    res.render('home.ejs', {emotes})
});

// Stream path to dispatch realtime events
app.get('/stream', async(req, res) => {
    try {
        // Setup stream connection
        res.writeHead(200, {
            'Content-Type': 'text/event-stream',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
        
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Origin, X-Requested-With, Content-Type, Accept',
        })
        // When 'push' event is seen send emote data {name, count} to the frontend
        Stream.on('push', (data) => {
            console.log(`data: ${JSON.stringify(data)}`)
            res.write(`data: ${JSON.stringify(data)}\n\n`)
        })
        // req.on('close', () => {
            // Stream.removeListener('push', )
        // })
    }
    catch (err) {
        res.status(500)
        console.log(`[SERVER] an error occured on /stream: ${err}`)
    }
})

app.listen(port, () => {
console.log(`SERVING UP A DELICIOUS APP ON PORT ${port}`);
});
