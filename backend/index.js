// Requirements
const express = require('express');
const mongoose = require('mongoose');
const emoteCount = require('./schemas/emotecounts');
// const { watch } = require('./middleware');
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
db.on("error", console.error.bind(console, "connection error:"));
db.once("open", () => {
    console.log("[SERVER] Database connected");
    // watch(emoteCount, getUpdatedCount => {
    //     // console.log(`[SERVER] DB UPDATED! ${JSON.stringify(change)}`)
    // })
});

const Stream = new EventEmitter()
// watch(emoteCount, getUpdatedCount)

async function getUpdatedCount(data) {
    try {
        const emote = await emoteCount.findById(data.documentKey._id)
        console.log(`[SERVER] ${emote.name} found in DB! New count is: ${emote.count}`)
        return emote
    }
    catch(e) {
        console.log(e)
        console.log(`[SERVER] ERROR! Could not find ${emote} in DB!`)
    }
}
// Create a change stream. The 'change' event gets emitted when there's a
// change in the database
const changeStream = emoteCount.watch()
    .on('change', async (data) =>  {
        emote = await getUpdatedCount(data)
        console.log(`ABOUT TO EMIT A PUSH EVENT WITH THIS DATA!\n${emote}`)
        Stream.emit("push", { name: emote.name, count: emote.count });
    });
    

app.get('/', (req, res) => {
    res.render('home.ejs')
});

app.get('/stream', async(req, res) => {
    console.log("STREAM GET SEEN!")
    res.writeHead(200, {
        'Content-Type': 'text/event-stream',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
    
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Origin, X-Requested-With, Content-Type, Accept',
      })
    Stream.on("push", (data) => {
        console.log("PUSH SEEN ON STREAM!")
        console.log(`data: ${JSON.stringify(data)}`)
        // res.write(JSON.stringify(data))
        res.write(`data: ${JSON.stringify(data)}\n\n`)
    })

    // try {
    //     req.on('close', () => {
    //         Stream.removeListener('push')
    //         // Stream.removeListener('updateEmotes', sendSse)
    //     })
    // } catch (err) {
    //     res.status(500)
    //     console.log(`[SERVER] an error occured on /stream: ${err}`)
    // }
})

app.listen(port, () => {
console.log(`SERVING UP A DELICIOUS APP ON PORT ${port}`);
});
