// Package Requirements
const express = require('express');
const mongoose = require('mongoose');

// Local Requirements
const emoteCount = require('./schemas/emotecounts');
const { EventEmitter } = require('events');

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
db.on("error", console.error.bind(console, "connection error:"));
db.once("open", () => {
    console.log("[SERVER] Database connected");
});

const Stream = new EventEmitter()

// Poll DB based on stream notification from mongo
async function getUpdatedCount(data) {
    try {
        // TODO: Is there a way to get the value directly from data.documentKey? To skip an extra DB Poll
        const emote = await emoteCount.findById(data.documentKey._id)
        console.log(`[SERVER] ${emote.name} found in DB! New count is: ${emote.count}`)
        return emote
    }
    catch(err) {
        console.log(`[SERVER] ERROR! Could not find emote in DB!`)
        console.log(err)
    }
}
// Create a change stream. The 'change' event gets emitted when there's a
// change in the database
const changeStream = emoteCount.watch()
    .on('change', async (data) =>  {
        // Poll DB to get updated values for change
        emote = await getUpdatedCount(data)
        // Send a 'push' event to /stream to be handled further in backend
        Stream.emit('push', { name: emote.name, count: emote.count });
    });
    

// Landing page (only planned page?)
app.get('/', (req, res) => {
    res.render('home.ejs')
});

// Stream path to dispatch realtime events
app.get('/stream', async(req, res) => {
    // Setup stream connection
    res.writeHead(200, {
        'Content-Type': 'text/event-stream',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
    
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Origin, X-Requested-With, Content-Type, Accept',
      })
    // When 'push' event is seen send emote data {name, count} to the frontend
    Stream.on("push", (data) => {
        console.log(`data: ${JSON.stringify(data)}`)
        res.write(`data: ${JSON.stringify(data)}\n\n`)
    })
    //TODO: Handle removing listeners when 'close' event is seen?
    // try {
    //     req.on('close', () => {
    //         Stream.removeListener('push')
    //     })
    // } catch (err) {
    //     res.status(500)
    //     console.log(`[SERVER] an error occured on /stream: ${err}`)
    // }
})

app.listen(port, () => {
console.log(`SERVING UP A DELICIOUS APP ON PORT ${port}`);
});
