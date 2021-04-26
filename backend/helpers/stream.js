// Package Requirements
const { EventEmitter } = require('events');
const mongoose = require('mongoose');

// Local Requirements
const emoteCount = require('../schemas/emotecounts');


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

module.exports = { Stream }