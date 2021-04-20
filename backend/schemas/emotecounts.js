const mongoose = require('mongoose')
const Schema = mongoose.Schema

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

module.exports = mongoose.model('emoteCount', emoteCountSchema, 'emoteCounts')
