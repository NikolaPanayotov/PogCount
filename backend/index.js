// Requirements
const express = require('express');
const mongoose = require('mongoose');
const emoteCount = require('./schemas/emotecounts');

// Express setup
const app = express();
const port = 3000;
app.set('view engine', 'ejs');

// Mongoose connection to DB
mongoose.connect('mongodb://mongo:27017/pogcount', {useNewUrlParser: true, 
                                                    useUnifiedTopology: true,
                                                    user: 'root',
                                                    pass: 'rootpassword',
                                                    authSource: 'admin'});x
const db = mongoose.connection;
db.on("error", console.error.bind(console, "connection error:"));
db.once("open", () => {
    console.log("Database connected");
});

app.get('/', async (req, res) => {
    res.render('home.ejs')
    const emoteCounts = await emoteCount.find({});
    console.log(emoteCounts);
});

app.listen(port, () => {
console.log(`SERVING UP A DELICIOUS APP ON PORT ${port}`);
});