// Requirements
const express = require('express');
const mongoose = require('mongoose');
const emoteCount = require('./schemas/emotecounts');

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
    console.log("Database connected");
});

async function updateCount(data) {
    try {
        emote = await emoteCount.findById(data.documentKey._id)
        console.log(`${emote.name} updated! New count is: ${emote.count}`)
    }
    catch(e) {
        console.log(e)
        console.log(`ERROR! Could not find ${emote} in DB!`)
    }
}

 // Create a change stream. The 'change' event gets emitted when there's a
  // change in the database
emoteCount.watch()
    .on('change', async (data) =>  {
        updateCount(data)
    });

app.get('/', async (req, res) => {
    res.render('home.ejs')
    const emoteCounts = await emoteCount.find({});
    console.log(emoteCounts);
});

app.listen(port, () => {
console.log(`SERVING UP A DELICIOUS APP ON PORT ${port}`);
});
