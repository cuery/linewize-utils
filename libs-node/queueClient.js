"use strict";
var sqs = require("./aws").SQS;
var config = require('config').config;
var MongoClient = require('mongodb').MongoClient;

function AWSQueueClient() {

}

AWSQueueClient.prototype.sendMessage = function(messageBody, queueUrl, next) {
    var message = {
        MessageBody: messageBody,
        QueueUrl: queueUrl
    };
    sqs.sendMessage(message, function(err) {
        if (err) {
            next(err);
        } else {
            next();
        }
    });
};

function LocalQueueClient() {
    var self = this;
    MongoClient.connect(config.MONGODB_INSTANCE + "/" + config.MONGODB_QUEUE_DB, function(err, db) {
        if (!err) {
            self.db = db;
        } else {
            console.log(err)
        }
    });
}

LocalQueueClient.prototype.sendMessage = function(messageBody, queue, next) {
    self.db.queue.insert({'inProg': False, 'done': False, 'msg': new Buffer(msg).toString('base64')})
}

function QueueClient(provider) {
    if (provider === "AWS") {
        return new AWSQueueClient();
    } else if (provider === "LOCAL") {
        return new LocalQueueClient();
    }
}

module.exports = QueueClient;
