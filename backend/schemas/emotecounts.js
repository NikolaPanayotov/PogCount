const mongoose = require('mongoose')
const Schema = mongoose.Schema

// Schema defines structure of each entry in database collection
const emoteCountSchema = new Schema({
    name: {
        type: String,
        required: true,
        unique: true
    },
    count: {
        type: Number,
        required: true
    },
    url: {
        type: String
    }
});

// Compile the schema to point to 'emoteCounts' 
module.exports = mongoose.model('emoteCount', emoteCountSchema, 'emoteCounts')
